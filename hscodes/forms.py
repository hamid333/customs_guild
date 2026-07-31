from django import forms

from .models import HSCode

TEXT_WIDGET_CLASS = "form-control"


class HSCodeSearchForm(forms.Form):
    q = forms.CharField(
        label="جست‌وجو",
        required=False,
        widget=forms.TextInput(attrs={
            "class": TEXT_WIDGET_CLASS,
            "placeholder": "کد تعرفه یا نام کالا را وارد کنید…",
        }),
    )


class HSCodeForm(forms.ModelForm):
    class Meta:
        model = HSCode
        fields = ["code", "title_fa", "title_en", "category", "duty_rate", "notes"]
        widgets = {
            "code": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "title_fa": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "title_en": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "category": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "duty_rate": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "notes": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 3}),
        }
