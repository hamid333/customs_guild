from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from .forms import SliderForm
from .models import Slider



class AjaxFormMixin:
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


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """دسترسی به داشبورد فقط برای کاربران staff مجاز است."""
    login_url = reverse_lazy("portal:dashboard_login")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff



# ---- بخش «اسلایدهای صفحه‌ی اصلی» در داشبورد (HeroSlide) --------------
class SlideDashListView(StaffRequiredMixin, ListView):
    model = Slider
    template_name = "Slider/slide_list.html"
    context_object_name = "slides"
    extra_context = {"active": "slides"}


class SlideCreateView(StaffRequiredMixin, AjaxFormMixin, CreateView):
    model = Slider
    form_class = SliderForm
    fragment_template_name = "Slider/fragments/_slide_fields.html"
    modal_title = "افزودن اسلاید جدید"
    success_url = reverse_lazy("slide_list")


class SlideUpdateView(StaffRequiredMixin, AjaxFormMixin, UpdateView):
    model = Slider
    form_class = SliderForm
    fragment_template_name = "Slider/fragments/_slide_fields.html"
    modal_title = "ویرایش اسلاید"
    success_url = reverse_lazy("slide_list")


class SlideDeleteView(StaffRequiredMixin, AjaxDeleteMixin, DeleteView):
    model = Slider
    template_name = "portal/dashboard/confirm_delete.html"
    success_url = reverse_lazy("slide_list")
