"""ویوهای عمومی و داشبورد برای نمونه‌کارها (CompletedWork)."""
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins import SectionAccessRequiredMixin, AjaxFormMixin, AjaxDeleteMixin

from .forms import CompletedWorkForm
from .models import CompletedWork


class CompletedWorkListView(ListView):
    """صفحه‌ی کارهای انجام‌شده (نمونه‌کارها) به همراه عضو مجریِ هرکدام."""
    model = CompletedWork
    template_name = "works/completed_works.html"
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


class WorkDashListView(SectionAccessRequiredMixin, ListView):
    required_section = "works"
    required_action = "view"
    model = CompletedWork
    template_name = "works/dashboard/work_list.html"
    context_object_name = "works"
    paginate_by = 20
    extra_context = {"active": "works"}


class WorkCreateView(SectionAccessRequiredMixin, AjaxFormMixin, CreateView):
    required_section = "works"
    required_action = "add"
    model = CompletedWork
    form_class = CompletedWorkForm
    fragment_template_name = "works/dashboard/fragments/_work_fields.html"
    modal_title = "افزودن نمونه‌کار"
    success_url = reverse_lazy("works:dash_work_list")


class WorkUpdateView(SectionAccessRequiredMixin, AjaxFormMixin, UpdateView):
    required_section = "works"
    required_action = "edit"
    model = CompletedWork
    form_class = CompletedWorkForm
    fragment_template_name = "works/dashboard/fragments/_work_fields.html"
    modal_title = "ویرایش نمونه‌کار"
    success_url = reverse_lazy("works:dash_work_list")


class WorkDeleteView(SectionAccessRequiredMixin, AjaxDeleteMixin, DeleteView):
    required_section = "works"
    required_action = "delete"
    model = CompletedWork
    template_name = "core/dashboard/confirm_delete.html"
    success_url = reverse_lazy("works:dash_work_list")
