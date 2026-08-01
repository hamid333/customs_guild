"""
میکسین‌های مشترک داشبورد که در تمام اپ‌های دیگر (members، news، works، hscodes،
sliders، specializations، contact) برای ویوهای Create/Update/Delete/List استفاده می‌شوند.

    StaffRequiredMixin        - فقط کاربران staff.
    SectionAccessRequiredMixin- علاوه بر staff بودن، کاربر باید دقیقاً همان عملیات
                                 (required_action: view/add/edit/delete) را روی همان
                                 بخش (required_section) مجاز داشته باشد. مدیران کل
                                 (superuser) همیشه به همه‌چیز دسترسی دارند.
    AjaxFormMixin              - افزودن/ویرایش با مودال SweetAlert2 + AJAX (به همراه
                                 fallback صفحه‌ی کامل برای درخواست‌های بدون جاوااسکریپت).
    AjaxDeleteMixin            - حذف با مودال تأیید SweetAlert2 + AJAX.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """دسترسی به داشبورد فقط برای کاربران staff مجاز است."""
    login_url = reverse_lazy("core:dashboard_login")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class SectionAccessRequiredMixin(StaffRequiredMixin):
    """هر ویو با ست‌کردن required_section و required_action مشخص می‌کند دقیقاً به کدام
    عملیات از کدام بخش داشبورد تعلق دارد؛ کاربر باید علاوه بر staff بودن، همان مجوز
    دقیق را هم داشته باشد. required_action پیش‌فرض «view» است (مناسب صفحات فهرست)."""
    required_section = None
    required_action = "view"

    def test_func(self):
        if not super().test_func():
            return False
        user = self.request.user
        if user.is_superuser:
            return True
        if not self.required_section:
            return True
        access = getattr(user, "dashboard_access", None)
        return bool(access and access.has_permission(self.required_section, self.required_action))


class AjaxFormMixin:
    """این میکسین به CreateView/UpdateView اضافه می‌شود تا امکان نمایش و ارسال فرم
    داخل مودال SweetAlert2 فراهم شود، بدون از دست رفتن قابلیت کار با صفحه‌ی کامل
    برای درخواست‌های غیر AJAX (fallback بدون جاوااسکریپت)."""

    fragment_template_name = None
    modal_title = ""
    template_name = "core/dashboard/generic_form_page.html"

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
            "core/dashboard/ajax/modal_form.html",
            {"form": form, "fragment_template": self.fragment_template_name, "object": getattr(self, "object", None)},
            request=self.request,
        )

    def get(self, request, *args, **kwargs):
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
    و درخواست AJAX نیز پشتیبانی شود.

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
