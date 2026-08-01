"""ویوهای داشبورد برای مدیریت زمینه‌های فعالیت (Specialization)."""
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins import SectionAccessRequiredMixin, AjaxFormMixin, AjaxDeleteMixin

from .forms import SpecializationForm
from .models import Specialization


class SpecializationDashListView(SectionAccessRequiredMixin, ListView):
    required_section = "specializations"
    required_action = "view"
    model = Specialization
    template_name = "specializations/dashboard/specialization_list.html"
    context_object_name = "specializations"
    paginate_by = 30
    extra_context = {"active": "specializations"}


class SpecializationCreateView(SectionAccessRequiredMixin, AjaxFormMixin, CreateView):
    required_section = "specializations"
    required_action = "add"
    model = Specialization
    form_class = SpecializationForm
    fragment_template_name = "specializations/dashboard/fragments/_specialization_fields.html"
    modal_title = "افزودن زمینه‌ی فعالیت"
    success_url = reverse_lazy("specializations:dash_specialization_list")


class SpecializationUpdateView(SectionAccessRequiredMixin, AjaxFormMixin, UpdateView):
    required_section = "specializations"
    required_action = "edit"
    model = Specialization
    form_class = SpecializationForm
    fragment_template_name = "specializations/dashboard/fragments/_specialization_fields.html"
    modal_title = "ویرایش زمینه‌ی فعالیت"
    success_url = reverse_lazy("specializations:dash_specialization_list")


class SpecializationDeleteView(SectionAccessRequiredMixin, AjaxDeleteMixin, DeleteView):
    required_section = "specializations"
    required_action = "delete"
    model = Specialization
    template_name = "core/dashboard/confirm_delete.html"
    success_url = reverse_lazy("specializations:dash_specialization_list")
