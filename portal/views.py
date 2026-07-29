"""
ویوهای سایت انجمن صنفی حق‌العمل‌کاران گمرکی.

بخش اول: صفحات عمومی (Home / اعضا / جست‌وجوی HS Code / اخبار / نمونه‌کارها / تماس با ما)
بخش دوم: داشبورد مدیریتی (ورود اطلاعات هر بخش) که فقط کاربران staff به آن دسترسی دارند.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, FormView,
    CreateView, UpdateView, DeleteView,
)

from .forms import (
    ContactForm, HSCodeSearchForm, MemberForm, NewsPostForm, CompletedWorkForm,
    HSCodeForm, StyledAuthenticationForm,
)
from .models import Member, HSCode, NewsPost, CompletedWork, ContactMessage, Specialization


# =====================================================================
# صفحات عمومی سایت (Public pages)
# =====================================================================

class HomeView(TemplateView):
    """صفحه‌ی اصلی (Home): معرفی انجمن، آمار، آخرین اخبار و نمونه‌کارهای شاخص."""
    template_name = "portal/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_members"] = Member.objects.filter(status=Member.STATUS_ACTIVE, is_featured=True)[:6]
        ctx["latest_news"] = NewsPost.objects.filter(is_published=True)[:3]
        ctx["latest_works"] = CompletedWork.objects.all()[:4]
        ctx["member_count"] = Member.objects.filter(status=Member.STATUS_ACTIVE).count()
        ctx["specializations"] = Specialization.objects.all()[:8]
        return ctx


class MemberListView(ListView):
    """صفحه‌ی اعضا: فهرست اعضای صنف به همراه زمینه‌ی فعالیت هرکدام و امکان فیلتر."""
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["stats"] = {
            "members": Member.objects.count(),
            "news": NewsPost.objects.count(),
            "works": CompletedWork.objects.count(),
            "hscodes": HSCode.objects.count(),
            "messages": ContactMessage.objects.filter(is_read=False).count(),
        }
        return ctx


# ---- بخش «اعضا» در داشبورد -----------------------------------------
class MemberDashListView(StaffRequiredMixin, ListView):
    model = Member
    template_name = "portal/dashboard/member_list.html"
    context_object_name = "members"
    paginate_by = 20


class MemberCreateView(StaffRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = "portal/dashboard/member_form.html"
    success_url = reverse_lazy("portal:dash_member_list")


class MemberUpdateView(StaffRequiredMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "portal/dashboard/member_form.html"
    success_url = reverse_lazy("portal:dash_member_list")


class MemberDeleteView(StaffRequiredMixin, DeleteView):
    model = Member
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("portal:dash_member_list")


# ---- بخش «اخبار» در داشبورد ------------------------------------------
class NewsDashListView(StaffRequiredMixin, ListView):
    model = NewsPost
    template_name = "portal/dashboard/news_list.html"
    context_object_name = "news_items"
    paginate_by = 20


class NewsCreateView(StaffRequiredMixin, CreateView):
    model = NewsPost
    form_class = NewsPostForm
    template_name = "portal/dashboard/news_form.html"
    success_url = reverse_lazy("portal:dash_news_list")


class NewsUpdateView(StaffRequiredMixin, UpdateView):
    model = NewsPost
    form_class = NewsPostForm
    template_name = "portal/dashboard/news_form.html"
    success_url = reverse_lazy("portal:dash_news_list")


class NewsDeleteView(StaffRequiredMixin, DeleteView):
    model = NewsPost
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("portal:dash_news_list")


# ---- بخش «نمونه‌کارها» در داشبورد ------------------------------------
class WorkDashListView(StaffRequiredMixin, ListView):
    model = CompletedWork
    template_name = "portal/dashboard/work_list.html"
    context_object_name = "works"
    paginate_by = 20


class WorkCreateView(StaffRequiredMixin, CreateView):
    model = CompletedWork
    form_class = CompletedWorkForm
    template_name = "portal/dashboard/work_form.html"
    success_url = reverse_lazy("portal:dash_work_list")


class WorkUpdateView(StaffRequiredMixin, UpdateView):
    model = CompletedWork
    form_class = CompletedWorkForm
    template_name = "portal/dashboard/work_form.html"
    success_url = reverse_lazy("portal:dash_work_list")


class WorkDeleteView(StaffRequiredMixin, DeleteView):
    model = CompletedWork
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("portal:dash_work_list")


# ---- بخش «ردیف‌های تعرفه» در داشبورد ---------------------------------
class HSCodeDashListView(StaffRequiredMixin, ListView):
    model = HSCode
    template_name = "portal/dashboard/hscode_list.html"
    context_object_name = "hscodes"
    paginate_by = 20


class HSCodeCreateView(StaffRequiredMixin, CreateView):
    model = HSCode
    form_class = HSCodeForm
    template_name = "portal/dashboard/hscode_form.html"
    success_url = reverse_lazy("portal:dash_hscode_list")


class HSCodeUpdateView(StaffRequiredMixin, UpdateView):
    model = HSCode
    form_class = HSCodeForm
    template_name = "portal/dashboard/hscode_form.html"
    success_url = reverse_lazy("portal:dash_hscode_list")


class HSCodeDeleteView(StaffRequiredMixin, DeleteView):
    model = HSCode
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("portal:dash_hscode_list")


# ---- بخش «پیام‌های تماس با ما» در داشبورد (فقط مشاهده / خواندن) -----
class ContactMessageDashListView(StaffRequiredMixin, ListView):
    model = ContactMessage
    template_name = "portal/dashboard/message_list.html"
    context_object_name = "contact_messages"
    paginate_by = 20


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
