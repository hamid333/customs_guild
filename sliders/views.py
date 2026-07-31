"""ویوهای داشبورد برای مدیریت اسلایدهای صفحه‌ی اصلی (HeroSlide)."""
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins import SectionAccessRequiredMixin, AjaxFormMixin, AjaxDeleteMixin

from .forms import HeroSlideForm
from .models import HeroSlide


class SlideDashListView(SectionAccessRequiredMixin, ListView):
    required_section = "sliders"
    model = HeroSlide
    template_name = "sliders/dashboard/slide_list.html"
    context_object_name = "slides"
    extra_context = {"active": "slides"}


class SlideCreateView(SectionAccessRequiredMixin, AjaxFormMixin, CreateView):
    required_section = "sliders"
    model = HeroSlide
    form_class = HeroSlideForm
    fragment_template_name = "sliders/dashboard/fragments/_slide_fields.html"
    modal_title = "افزودن اسلاید جدید"
    success_url = reverse_lazy("sliders:dash_slide_list")


class SlideUpdateView(SectionAccessRequiredMixin, AjaxFormMixin, UpdateView):
    required_section = "sliders"
    model = HeroSlide
    form_class = HeroSlideForm
    fragment_template_name = "sliders/dashboard/fragments/_slide_fields.html"
    modal_title = "ویرایش اسلاید"
    success_url = reverse_lazy("sliders:dash_slide_list")


class SlideDeleteView(SectionAccessRequiredMixin, AjaxDeleteMixin, DeleteView):
    required_section = "sliders"
    model = HeroSlide
    template_name = "core/dashboard/confirm_delete.html"
    success_url = reverse_lazy("sliders:dash_slide_list")
