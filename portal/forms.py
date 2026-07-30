"""
فرم‌های سایت:
    - ContactForm     : فرم عمومی «تماس با ما»
    - HSCodeSearchForm: فرم جست‌وجوی ردیف تعرفه
    - فرم‌های داشبورد برای ورود اطلاعات هر بخش (اعضا، اخبار، نمونه‌کارها، تعرفه‌ها، زمینه‌های فعالیت، اسلایدها)

نکات:
    - فیلدهایی با کلاس CSS «select2-field» توسط static/portal/js/dashboard.js با کتابخانه‌ی
      Select2 مقداردهی اولیه می‌شوند.
    - فیلدهایی با کلاس «jalali-datepicker» / «jalali-datetimepicker» یک ورودی متنی ساده هستند
      که با persian-datepicker به تقویم شمسی مجهز می‌شوند؛ مقدار متنی توسط فرم فیلد
      jDateField/jDateTimeField کتابخانه‌ی django-jalali پردازش و به تاریخ میلادی تبدیل می‌شود.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    ContactMessage, NewsPost, CompletedWork, HSCode
)

# کلاس‌های CSS مشترک برای یک‌دستی ظاهر فرم‌ها
TEXT_WIDGET_CLASS = "form-control"
SELECT2_WIDGET_CLASS = "form-control select2-field"
JALALI_DATE_CLASS = "form-control jalali-datepicker"
JALALI_DATETIME_CLASS = "form-control jalali-datetimepicker"


class StyledAuthenticationForm(AuthenticationForm):
    """فرم ورود داشبورد با کلاس‌های CSS یک‌دست با بقیه‌ی سایت."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": TEXT_WIDGET_CLASS, "placeholder": "نام کاربری"})
        self.fields["password"].widget.attrs.update({"class": TEXT_WIDGET_CLASS, "placeholder": "رمز عبور"})


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


class HSCodeSearchForm(forms.Form):
    q = forms.CharField(
        label="جست‌وجو",
        required=False,
        widget=forms.TextInput(attrs={
            "class": TEXT_WIDGET_CLASS,
            "placeholder": "کد تعرفه یا نام کالا را وارد کنید…",
            "placeholder": "کد تعرفه یا نام کالا را وارد کنید…",
        }),
    )


# ---------------------------------------------------------------
# فرم‌های داشبورد مدیریتی (ورود اطلاعات هر بخش)
# ---------------------------------------------------------------


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



