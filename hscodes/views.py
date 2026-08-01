"""ویوهای عمومی و داشبورد برای ردیف‌های تعرفه (HS Code)."""
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins import SectionAccessRequiredMixin, AjaxFormMixin, AjaxDeleteMixin

from .forms import HSCodeSearchForm, HSCodeForm
from .models import HSCode


class HSCodeSearchView(ListView):
    """صفحه‌ی جست‌وجوی ردیف تعرفه‌ی گمرکی (HS Code)."""
    model = HSCode
    template_name = "hscodes/hs_code_search.html"
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


class HSCodeDashListView(SectionAccessRequiredMixin, ListView):
    required_section = "hscodes"
    required_action = "view"
    model = HSCode
    template_name = "hscodes/dashboard/hscode_list.html"
    context_object_name = "hscodes"
    paginate_by = 20
    extra_context = {"active": "hscodes"}


class HSCodeCreateView(SectionAccessRequiredMixin, AjaxFormMixin, CreateView):
    required_section = "hscodes"
    required_action = "add"
    model = HSCode
    form_class = HSCodeForm
    fragment_template_name = "hscodes/dashboard/fragments/_hscode_fields.html"
    modal_title = "افزودن ردیف تعرفه"
    success_url = reverse_lazy("hscodes:dash_hscode_list")


class HSCodeUpdateView(SectionAccessRequiredMixin, AjaxFormMixin, UpdateView):
    required_section = "hscodes"
    required_action = "edit"
    model = HSCode
    form_class = HSCodeForm
    fragment_template_name = "hscodes/dashboard/fragments/_hscode_fields.html"
    modal_title = "ویرایش ردیف تعرفه"
    success_url = reverse_lazy("hscodes:dash_hscode_list")


class HSCodeDeleteView(SectionAccessRequiredMixin, AjaxDeleteMixin, DeleteView):
    required_section = "hscodes"
    required_action = "delete"
    model = HSCode
    template_name = "core/dashboard/confirm_delete.html"
    success_url = reverse_lazy("hscodes:dash_hscode_list")
