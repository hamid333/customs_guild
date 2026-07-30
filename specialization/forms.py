from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    Specialization
)

# کلاس‌های CSS مشترک برای یک‌دستی ظاهر فرم‌ها
TEXT_WIDGET_CLASS = "form-control"
SELECT2_WIDGET_CLASS = "form-control select2-field"




class SpecializationForm(forms.ModelForm):
    """فرم افزودن/ویرایش دستی زمینه‌ی فعالیت (Specialization) از داشبورد."""

    class Meta:
        model = Specialization
        fields = ["title", "slug"]
        widgets = {
            "title": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "مثلاً: ترخیص کالای صنعتی"}),
            "slug": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "اختیاری - در صورت خالی بودن خودکار ساخته می‌شود"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False

    def clean_slug(self):
        from django.utils.text import slugify
        slug = self.cleaned_data.get("slug", "").strip()
        if not slug:
            slug = slugify(self.cleaned_data.get("title", ""), allow_unicode=True)
        return slug

