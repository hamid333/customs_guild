"""
ویوهای اپ core:
    - HomeView: صفحه‌ی اصلی سایت (اسلایدر + آمار + آخرین اخبار/نمونه‌کارها) — داده‌ها را
      از اپ‌های دیگر (sliders، members، news، works، specializations) جمع می‌کند.
    - DashboardLoginView / DashboardLogoutView / DashboardHomeView
    - مدیریت کاربران داشبورد (افزودن/ویرایش/حذف + تعیین دسترسی بخش‌ها)
"""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView

from .forms import StyledAuthenticationForm, DashboardUserForm
from .mixins import StaffRequiredMixin, SectionAccessRequiredMixin, AjaxDeleteMixin

User = get_user_model()


class HomeView(TemplateView):
    """صفحه‌ی اصلی (Home): اسلایدر، معرفی انجمن، آمار، آخرین اخبار و نمونه‌کارهای شاخص."""
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        from sliders.models import HeroSlide
        from members.models import Member
        from news.models import NewsPost
        from works.models import CompletedWork
        from specializations.models import Specialization

        ctx = super().get_context_data(**kwargs)
        ctx["hero_slides"] = HeroSlide.objects.filter(is_active=True)
        ctx["featured_members"] = Member.objects.filter(status=Member.STATUS_ACTIVE, is_featured=True)[:6]
        ctx["latest_news"] = NewsPost.objects.filter(is_published=True)[:3]
        ctx["latest_works"] = CompletedWork.objects.all()[:4]
        ctx["member_count"] = Member.objects.filter(status=Member.STATUS_ACTIVE).count()
        ctx["specializations"] = Specialization.objects.all()[:8]
        return ctx


class DashboardLoginView(LoginView):
    template_name = "core/dashboard/login.html"
    redirect_authenticated_user = True
    authentication_form = StyledAuthenticationForm


class DashboardLogoutView(LogoutView):
    next_page = "core:home"


class DashboardHomeView(StaffRequiredMixin, TemplateView):
    """صفحه‌ی اصلی داشبورد: آمار کلی و دسترسی سریع به ورود اطلاعات هر بخش."""
    template_name = "core/dashboard/home.html"
    extra_context = {"active": "home"}

    def get_context_data(self, **kwargs):
        from members.models import Member
        from news.models import NewsPost
        from works.models import CompletedWork
        from hscodes.models import HSCode
        from specializations.models import Specialization
        from sliders.models import HeroSlide
        from contact.models import ContactMessage

        ctx = super().get_context_data(**kwargs)
        ctx["stats"] = {
            "members": Member.objects.count(),
            "news": NewsPost.objects.count(),
            "works": CompletedWork.objects.count(),
            "hscodes": HSCode.objects.count(),
            "specializations": Specialization.objects.count(),
            "slides": HeroSlide.objects.count(),
            "messages": ContactMessage.objects.filter(is_read=False).count(),
            "users": User.objects.filter(is_staff=True).count(),
        }
        return ctx


# =====================================================================
# مدیریت کاربران داشبورد (افزودن/ویرایش/حذف + تعیین دسترسی بخش‌ها)
# =====================================================================

class UserAccessRequiredMixin(SectionAccessRequiredMixin):
    required_section = "users"


class UserDashListView(UserAccessRequiredMixin, ListView):
    model = User
    template_name = "core/dashboard/user_list.html"
    context_object_name = "dash_users"
    extra_context = {"active": "users"}

    def get_queryset(self):
        return User.objects.filter(is_staff=True).select_related("dashboard_access").order_by("username")


class _UserFormAjaxHelper:
    """کمکی مشترک برای افزودن/ویرایش کاربر با پشتیبانی از مودال SweetAlert2 + AJAX
    (مشابه core.mixins.AjaxFormMixin اما چون DashboardUserForm یک ModelForm معمولی
    نیست، این‌جا به‌صورت دستی پیاده‌سازی شده است)."""

    fragment_template_name = "core/dashboard/fragments/_user_fields.html"
    success_url = reverse_lazy("core:dash_user_list")

    def is_ajax(self):
        return self.request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def render_modal_fragment(self, form):
        return render_to_string(
            "core/dashboard/ajax/modal_form.html",
            {"form": form, "fragment_template": self.fragment_template_name},
            request=self.request,
        )

    def render_full_page(self, form, page_title):
        return render(self.request, "core/dashboard/generic_form_page.html", {
            "form": form,
            "fragment_template": self.fragment_template_name,
            "page_title": page_title,
            "cancel_url": self.success_url,
            "active": "users",
        })


class UserCreateView(UserAccessRequiredMixin, _UserFormAjaxHelper, View):
    page_title = "افزودن کاربر جدید"

    def get(self, request):
        form = DashboardUserForm()
        if self.is_ajax():
            return HttpResponse(self.render_modal_fragment(form))
        return self.render_full_page(form, self.page_title)

    def post(self, request):
        form = DashboardUserForm(request.POST)
        if form.is_valid():
            form.save()
            if self.is_ajax():
                return JsonResponse({"success": True})
            messages.success(request, "کاربر با موفقیت ایجاد شد.")
            return redirect(self.success_url)
        if self.is_ajax():
            return JsonResponse({"success": False, "html": self.render_modal_fragment(form)}, status=400)
        return self.render_full_page(form, self.page_title)


class UserUpdateView(UserAccessRequiredMixin, _UserFormAjaxHelper, View):
    page_title = "ویرایش کاربر و دسترسی‌ها"

    def get(self, request, pk):
        user_obj = get_object_or_404(User, pk=pk)
        form = DashboardUserForm(instance=user_obj)
        if self.is_ajax():
            return HttpResponse(self.render_modal_fragment(form))
        return self.render_full_page(form, self.page_title)

    def post(self, request, pk):
        user_obj = get_object_or_404(User, pk=pk)
        form = DashboardUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            if self.is_ajax():
                return JsonResponse({"success": True})
            messages.success(request, "تغییرات کاربر ذخیره شد.")
            return redirect(self.success_url)
        if self.is_ajax():
            return JsonResponse({"success": False, "html": self.render_modal_fragment(form)}, status=400)
        return self.render_full_page(form, self.page_title)


class UserDeleteView(UserAccessRequiredMixin, AjaxDeleteMixin, DeleteView):
    model = User
    template_name = "core/dashboard/confirm_delete.html"
    success_url = reverse_lazy("core:dash_user_list")
    extra_context = {"active": "users"}

    def form_valid(self, form):
        if self.object.pk == self.request.user.pk:
            message = "نمی‌توانید حساب کاربری خودتان را حذف کنید."
            if self.is_ajax():
                return JsonResponse({"success": False, "error": message}, status=400)
            messages.error(self.request, message)
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)
