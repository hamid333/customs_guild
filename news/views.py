"""ویوهای عمومی و داشبورد برای اخبار."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.mixins import SectionAccessRequiredMixin, AjaxFormMixin, AjaxDeleteMixin

from .forms import NewsPostForm
from .models import NewsPost


class NewsListView(ListView):
    """صفحه‌ی اخبار سایت."""
    model = NewsPost
    template_name = "news/news_list.html"
    context_object_name = "news_items"
    paginate_by = 9

    def get_queryset(self):
        return NewsPost.objects.filter(is_published=True)


class NewsDetailView(DetailView):
    model = NewsPost
    template_name = "news/news_detail.html"
    context_object_name = "news"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return NewsPost.objects.filter(is_published=True)


class NewsDashListView(SectionAccessRequiredMixin, ListView):
    required_section = "news"
    required_action = "view"
    model = NewsPost
    template_name = "news/dashboard/news_list.html"
    context_object_name = "news_items"
    paginate_by = 20
    extra_context = {"active": "news"}


class NewsCreateView(SectionAccessRequiredMixin, AjaxFormMixin, CreateView):
    required_section = "news"
    required_action = "add"
    model = NewsPost
    form_class = NewsPostForm
    fragment_template_name = "news/dashboard/fragments/_news_fields.html"
    modal_title = "افزودن خبر جدید"
    success_url = reverse_lazy("news:dash_news_list")


class NewsUpdateView(SectionAccessRequiredMixin, AjaxFormMixin, UpdateView):
    required_section = "news"
    required_action = "edit"
    model = NewsPost
    form_class = NewsPostForm
    fragment_template_name = "news/dashboard/fragments/_news_fields.html"
    modal_title = "ویرایش خبر"
    success_url = reverse_lazy("news:dash_news_list")


class NewsDeleteView(SectionAccessRequiredMixin, AjaxDeleteMixin, DeleteView):
    required_section = "news"
    required_action = "delete"
    model = NewsPost
    template_name = "core/dashboard/confirm_delete.html"
    success_url = reverse_lazy("news:dash_news_list")
