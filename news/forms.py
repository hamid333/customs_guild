from django import forms

from .models import NewsPost

TEXT_WIDGET_CLASS = "form-control"
JALALI_DATETIME_CLASS = "form-control jalali-datetimepicker"


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ["title", "slug", "summary", "body", "cover_image", "is_published", "published_at"]
        widgets = {
            "title": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "slug": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "مثال: khabar-jadid"}),
            "summary": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "body": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 8}),
            "published_at": forms.TextInput(attrs={
                "class": JALALI_DATETIME_CLASS,
                "placeholder": "مثال: ۱۴۰۴/۰۵/۱۰ ۱۴:۳۰",
                "autocomplete": "off",
            }),
        }
