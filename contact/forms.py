from django import forms

from .models import ContactMessage

TEXT_WIDGET_CLASS = "form-control"


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "نام و نام خانوادگی"}),
            "email": forms.EmailInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "ایمیل"}),
            "phone": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "شماره تماس (اختیاری)"}),
            "subject": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "موضوع پیام"}),
            "message": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 5, "placeholder": "متن پیام شما..."}),
        }
