"""ویوهای عمومی و داشبورد برای تماس با ما."""
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView

from core.mixins import SectionAccessRequiredMixin

from .forms import ContactForm
from .models import ContactMessage


class ContactView(FormView):
    """صفحه‌ی تماس با ما."""
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact:contact")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "پیام شما با موفقیت ارسال شد. همکاران ما در اسرع وقت پاسخ‌گو خواهند بود.")
        return super().form_valid(form)


class ContactMessageDashListView(SectionAccessRequiredMixin, ListView):
    required_section = "contact"
    model = ContactMessage
    template_name = "contact/dashboard/message_list.html"
    context_object_name = "contact_messages"
    paginate_by = 20
    extra_context = {"active": "messages"}


class ContactMessageDetailView(SectionAccessRequiredMixin, DetailView):
    required_section = "contact"
    model = ContactMessage
    template_name = "contact/dashboard/message_detail.html"
    context_object_name = "contact_message"
    extra_context = {"active": "messages"}

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.is_read:
            self.object.is_read = True
            self.object.save(update_fields=["is_read"])
        return response
