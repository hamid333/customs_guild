from django import forms

from .models import HeroSlide

# کلاس‌های CSS مشترک برای یک‌دستی ظاهر فرم‌ها
TEXT_WIDGET_CLASS = "form-control"



class HeroSlideForm(forms.ModelForm):
    """فرم مدیریت اسلایدهای اسلایدر صفحه‌ی اصلی. تمام فیلدها اختیاری هستند."""

    class Meta:
        model = HeroSlide
        fields = ["eyebrow", "title", "description", "image", "button_text", "button_url", "order", "is_active"]
        widgets = {
            "eyebrow": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "مثلاً: خدمات آنلاین (اختیاری)"}),
            "title": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "تیتر اصلی اسلاید (اختیاری)"}),
            "description": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 3, "placeholder": "متن توضیح (اختیاری)"}),
            "button_text": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "مثلاً: مشاهده‌ی اعضا (اختیاری)"}),
            "button_url": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "/members/ یا https://... (اختیاری)"}),
            "order": forms.NumberInput(attrs={"class": TEXT_WIDGET_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            if name != "is_active":
                self.fields[name].required = False
