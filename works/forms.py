from django import forms

from .models import CompletedWork

TEXT_WIDGET_CLASS = "form-control"
SELECT2_WIDGET_CLASS = "form-control select2-field"
JALALI_DATE_CLASS = "form-control jalali-datepicker"


class CompletedWorkForm(forms.ModelForm):
    class Meta:
        model = CompletedWork
        fields = ["title", "member", "category", "description", "image", "completed_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "member": forms.Select(attrs={"class": SELECT2_WIDGET_CLASS}),
            "category": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "description": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 5}),
            "completed_date": forms.TextInput(attrs={
                "class": JALALI_DATE_CLASS,
                "placeholder": "مثال: ۱۴۰۴/۰۵/۱۰",
                "autocomplete": "off",
            }),
        }
