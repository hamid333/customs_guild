
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, FormView,
    CreateView, UpdateView, DeleteView,
)

from member.models import Member
from specialization.models import Specialization


from .forms import (ContactForm, HSCodeSearchForm, NewsPostForm, CompletedWorkForm, HSCodeForm, HeroSlideForm, StyledAuthenticationForm)
from .models import (HSCode, NewsPost, CompletedWork, ContactMessage, HeroSlide)


# =====================================================================
# صفحات عمومی سایت (Public pages)
# =====================================================================

class HomeView(TemplateView):
    """صفحه‌ی اصلی (Home): اسلایدر، معرفی انجمن، آمار، آخرین اخبار و نمونه‌کارهای شاخص."""
    template_name = "portal/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["hero_slides"] = HeroSlide.objects.filter(is_active=True)
        ctx["featured_members"] = Member.objects.filter(status=Member.STATUS_ACTIVE, is_featured=True)[:6]
        ctx["latest_news"] = NewsPost.objects.filter(is_published=True)[:3]
        ctx["latest_works"] = CompletedWork.objects.all()[:4]
        ctx["member_count"] = Member.objects.filter(status=Member.STATUS_ACTIVE).count()
        ctx["specializations"] = Specialization.objects.all()[:8]
        return ctx


class MemberListView(ListView):
    """صفحه‌ی «همه‌ی اعضا»: فهرست کامل اعضای صنف به همراه زمینه‌ی فعالیت هرکدام و امکان فیلتر."""
    model = Member
    template_name = "portal/members.html"
    context_object_name = "members"
    paginate_by = 12

    def get_queryset(self):
        qs = Member.objects.filter(status=Member.STATUS_ACTIVE).prefetch_related("specializations")
        q = self.request.GET.get("q", "").strip()
        spec = self.request.GET.get("spec", "").strip()
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(city__icontains=q) | Q(membership_no__icontains=q))
        if spec:
            qs = qs.filter(specializations__slug=spec)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["specializations"] = Specialization.objects.all()
        ctx["current_q"] = self.request.GET.get("q", "")
        ctx["current_spec"] = self.request.GET.get("spec", "")
        return ctx


class FeaturedMemberListView(ListView):
    """صفحه‌ی «اعضای اصلی»: فقط اعضایی که برای نمایش ویژه علامت‌گذاری شده‌اند (is_featured)."""
    model = Member
    template_name = "portal/featured_members.html"
    context_object_name = "members"

    def get_queryset(self):
        return (
            Member.objects.filter(status=Member.STATUS_ACTIVE, is_featured=True)
            .prefetch_related("specializations")
        )


class MemberDetailView(DetailView):
    """پروفایل هر عضو؛ زمینه‌های فعالیت و نمونه‌کارهای همان عضو نمایش داده می‌شود."""
    model = Member
    template_name = "portal/member_detail.html"
    context_object_name = "member"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["works"] = self.object.completed_works.all()
        return ctx


class HSCodeSearchView(ListView):
    """صفحه‌ی جست‌وجوی ردیف تعرفه‌ی گمرکی (HS Code)."""
    model = HSCode
    template_name = "portal/hs_code_search.html"
    context_object_name = "results"
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if not q:
            return HSCode.objects.none()
        return HSCode.objects.filter(
            Q(code__icontains=q) | Q(title_fa__icontains=q) |
            Q(title_en__icontains=q) | Q(category__icontains=q)
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = HSCodeSearchForm(initial={"q": self.request.GET.get("q", "")})
        ctx["query"] = self.request.GET.get("q", "").strip()
        return ctx


class NewsListView(ListView):
    """صفحه‌ی اخبار سایت."""
    model = NewsPost
    template_name = "portal/news_list.html"
    context_object_name = "news_items"
    paginate_by = 9

    def get_queryset(self):
        return NewsPost.objects.filter(is_published=True)


class NewsDetailView(DetailView):
    model = NewsPost
    template_name = "portal/news_detail.html"
    context_object_name = "news"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return NewsPost.objects.filter(is_published=True)


class CompletedWorkListView(ListView):
    """صفحه‌ی کارهای انجام‌شده (نمونه‌کارها) به همراه عضو مجریِ هرکدام."""
    model = CompletedWork
    template_name = "portal/completed_works.html"
    context_object_name = "works"
    paginate_by = 9

    def get_queryset(self):
        qs = CompletedWork.objects.select_related("member")
        cat = self.request.GET.get("cat", "").strip()
        if cat:
            qs = qs.filter(category__iexact=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = (
            CompletedWork.objects.exclude(category="").values_list("category", flat=True).distinct()
        )
        ctx["current_cat"] = self.request.GET.get("cat", "")
        return ctx


class ContactView(FormView):
    """صفحه‌ی تماس با ما."""
    template_name = "portal/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("portal:contact")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "پیام شما با موفقیت ارسال شد. همکاران ما در اسرع وقت پاسخ‌گو خواهند بود.")
        return super().form_valid(form)


# =====================================================================
# میکسین‌های عمومی برای ثبت/ویرایش/حذف با مودال (SweetAlert2 + AJAX)
# =====================================================================

class AjaxFormMixin:
    """این میکسین به CreateView/UpdateView اضافه می‌شود تا امکان نمایش و ارسال فرم
    داخل مودال SweetAlert2 فراهم شود، بدون از دست رفتن قابلیت کار با صفحه‌ی کامل
    برای درخواست‌های غیر AJAX (fallback بدون جاوااسکریپت)."""

    fragment_template_name = None   # مسیر تمپلیتی که فقط شامل ردیف‌های فیلد است (بدون تگ <form>)
    modal_title = ""                # عنوانی که در مودال نمایش داده می‌شود
    template_name = "portal/dashboard/generic_form_page.html"  # قالب مشترک صفحه‌ی کامل (fallback)

    def is_ajax(self):
        return self.request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["fragment_template"] = self.fragment_template_name
        ctx["page_title"] = self.modal_title
        ctx["cancel_url"] = self.get_success_url()
        return ctx

    def render_modal_fragment(self, form):
        return render_to_string(
            "portal/dashboard/ajax/modal_form.html",
            {"form": form, "fragment_template": self.fragment_template_name, "object": getattr(self, "object", None)},
            request=self.request,
        )

    def get(self, request, *args, **kwargs):
        # برای UpdateView شیء موجود را لود می‌کنیم؛ برای CreateView مقدار None باقی می‌ماند.
        if "pk" in self.kwargs or "slug" in self.kwargs:
            self.object = self.get_object()
        else:
            self.object = None
        if self.is_ajax():
            form = self.get_form()
            return HttpResponse(self.render_modal_fragment(form))
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({"success": False, "html": self.render_modal_fragment(form)}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.is_ajax():
            return JsonResponse({"success": True})
        return response


class AjaxDeleteMixin:
    """این میکسین به DeleteView اضافه می‌شود تا حذف از طریق مودال تأیید SweetAlert2
    و درخواست AJAX نیز پشتیبانی شود؛ حذف مستقیم از طریق صفحه‌ی تأیید (بدون جاوااسکریپت) نیز کار می‌کند.

    نکته‌ی نسخه: از Django 4.0 به بعد، DeleteView بر پایه‌ی FormMixin است و حذف واقعی در
    form_valid() انجام می‌شود (نه در متد قدیمی‌تر delete())، چون BaseDeleteView.post()
    مستقیماً form_valid() را صدا می‌زند. به همین دلیل اینجا form_valid() بازنویسی شده است."""

    def is_ajax(self):
        return self.request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        if self.is_ajax():
            return JsonResponse({"success": True})
        return HttpResponseRedirect(success_url)


# =====================================================================
# داشبورد مدیریتی (Dashboard) — فقط برای کاربران staff
# =====================================================================

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """دسترسی به داشبورد فقط برای کاربران staff مجاز است."""
    login_url = reverse_lazy("portal:dashboard_login")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class DashboardLoginView(LoginView):
    template_name = "portal/dashboard/login.html"
    redirect_authenticated_user = True
    authentication_form = StyledAuthenticationForm


class DashboardLogoutView(LogoutView):
    next_page = "portal:home"


class DashboardHomeView(StaffRequiredMixin, TemplateView):
    """صفحه‌ی اصلی داشبورد: آمار کلی و دسترسی سریع به ورود اطلاعات هر بخش."""
    template_name = "portal/dashboard/home.html"
    extra_context = {"active": "home"}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["stats"] = {
            "members": Member.objects.count(),
            "news": NewsPost.objects.count(),
            "works": CompletedWork.objects.count(),
            "hscodes": HSCode.objects.count(),
            "specializations": Specialization.objects.count(),
            "slides": HeroSlide.objects.count(),
            "messages": ContactMessage.objects.filter(is_read=False).count(),
        }
        return ctx


# ---- بخش «اخبار» در داشبورد ------------------------------------------
class NewsDashListView(StaffRequiredMixin, ListView):
    model = NewsPost
    template_name = "portal/dashboard/news_list.html"
    context_object_name = "news_items"
    paginate_by = 20
    extra_context = {"active": "news"}


class NewsCreateView(StaffRequiredMixin, AjaxFormMixin, CreateView):
    model = NewsPost
    form_class = NewsPostForm
    fragment_template_name = "portal/dashboard/fragments/_news_fields.html"
    modal_title = "افزودن خبر جدید"
    success_url = reverse_lazy("portal:dash_news_list")


class NewsUpdateView(StaffRequiredMixin, AjaxFormMixin, UpdateView):
    model = NewsPost
    form_class = NewsPostForm
    fragment_template_name = "portal/dashboard/fragments/_news_fields.html"
    modal_title = "ویرایش خبر"
    success_url = reverse_lazy("portal:dash_news_list")


class NewsDeleteView(StaffRequiredMixin, AjaxDeleteMixin, DeleteView):
    model = NewsPost
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("portal:dash_news_list")


# ---- بخش «نمونه‌کارها» در داشبورد ------------------------------------
class WorkDashListView(StaffRequiredMixin, ListView):
    model = CompletedWork
    template_name = "portal/dashboard/work_list.html"
    context_object_name = "works"
    paginate_by = 20
    extra_context = {"active": "works"}


class WorkCreateView(StaffRequiredMixin, AjaxFormMixin, CreateView):
    model = CompletedWork
    form_class = CompletedWorkForm
    fragment_template_name = "portal/dashboard/fragments/_work_fields.html"
    modal_title = "افزودن نمونه‌کار"
    success_url = reverse_lazy("portal:dash_work_list")


class WorkUpdateView(StaffRequiredMixin, AjaxFormMixin, UpdateView):
    model = CompletedWork
    form_class = CompletedWorkForm
    fragment_template_name = "portal/dashboard/fragments/_work_fields.html"
    modal_title = "ویرایش نمونه‌کار"
    success_url = reverse_lazy("portal:dash_work_list")


class WorkDeleteView(StaffRequiredMixin, AjaxDeleteMixin, DeleteView):
    model = CompletedWork
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("portal:dash_work_list")


# ---- بخش «ردیف‌های تعرفه» در داشبورد ---------------------------------
class HSCodeDashListView(StaffRequiredMixin, ListView):
    model = HSCode
    template_name = "portal/dashboard/hscode_list.html"
    context_object_name = "hscodes"
    paginate_by = 20
    extra_context = {"active": "hscodes"}


class HSCodeCreateView(StaffRequiredMixin, AjaxFormMixin, CreateView):
    model = HSCode
    form_class = HSCodeForm
    fragment_template_name = "portal/dashboard/fragments/_hscode_fields.html"
    modal_title = "افزودن ردیف تعرفه"
    success_url = reverse_lazy("portal:dash_hscode_list")


class HSCodeUpdateView(StaffRequiredMixin, AjaxFormMixin, UpdateView):
    model = HSCode
    form_class = HSCodeForm
    fragment_template_name = "portal/dashboard/fragments/_hscode_fields.html"
    modal_title = "ویرایش ردیف تعرفه"
    success_url = reverse_lazy("portal:dash_hscode_list")


class HSCodeDeleteView(StaffRequiredMixin, AjaxDeleteMixin, DeleteView):
    model = HSCode
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("portal:dash_hscode_list")



# ---- بخش «اسلایدهای صفحه‌ی اصلی» در داشبورد (HeroSlide) --------------
class SlideDashListView(StaffRequiredMixin, ListView):
    model = HeroSlide
    template_name = "portal/dashboard/slide_list.html"
    context_object_name = "slides"
    extra_context = {"active": "slides"}


class SlideCreateView(StaffRequiredMixin, AjaxFormMixin, CreateView):
    model = HeroSlide
    form_class = HeroSlideForm
    fragment_template_name = "portal/dashboard/fragments/_slide_fields.html"
    modal_title = "افزودن اسلاید جدید"
    success_url = reverse_lazy("portal:dash_slide_list")


class SlideUpdateView(StaffRequiredMixin, AjaxFormMixin, UpdateView):
    model = HeroSlide
    form_class = HeroSlideForm
    fragment_template_name = "portal/dashboard/fragments/_slide_fields.html"
    modal_title = "ویرایش اسلاید"
    success_url = reverse_lazy("portal:dash_slide_list")


class SlideDeleteView(StaffRequiredMixin, AjaxDeleteMixin, DeleteView):
    model = HeroSlide
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("portal:dash_slide_list")


# ---- بخش «پیام‌های تماس با ما» در داشبورد (فقط مشاهده / خواندن) -----
class ContactMessageDashListView(StaffRequiredMixin, ListView):
    model = ContactMessage
    template_name = "portal/dashboard/message_list.html"
    context_object_name = "contact_messages"
    paginate_by = 20
    extra_context = {"active": "messages"}


class ContactMessageDetailView(StaffRequiredMixin, DetailView):
    model = ContactMessage
    template_name = "portal/dashboard/message_detail.html"
    context_object_name = "contact_message"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.is_read:
            self.object.is_read = True
            self.object.save(update_fields=["is_read"])
        return response
