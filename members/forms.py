from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Member

TEXT_WIDGET_CLASS = "form-control"
SELECT2_WIDGET_CLASS = "form-control select2-field"


class MemberForm(forms.ModelForm):
    bio = forms.CharField(
        label="درباره / سوابق فعالیت",
        required=False,
        widget=CKEditorWidget(config_name="default"),
        help_text="هر عضو می‌تواند سوابق فعالیت خودش را با متن غنی (تیتر، لیست، رنگ، تصویر و ...) زیبا طراحی کند.",
    )

    class Meta:
        model = Member
        fields = [
            "full_name", "membership_no", "license_no", "role", "specializations",
            "photo", "phone", "email", "city", "address", "bio",
            "established_year", "status", "is_featured",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "membership_no": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "license_no": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "role": forms.Select(attrs={"class": SELECT2_WIDGET_CLASS}),
            "specializations": forms.SelectMultiple(attrs={"class": SELECT2_WIDGET_CLASS}),
            "phone": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "email": forms.EmailInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "city": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "address": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "established_year": forms.NumberInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "status": forms.Select(attrs={"class": SELECT2_WIDGET_CLASS}),
        }
