"""
فرم‌های سایت:
    - ContactForm     : فرم عمومی «تماس با ما»
    - HSCodeSearchForm: فرم جست‌وجوی ردیف تعرفه
    - فرم‌های داشبورد برای ورود اطلاعات هر بخش (اعضا، اخبار، نمونه‌کارها، تعرفه‌ها)
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import ContactMessage, Member, NewsPost, CompletedWork, HSCode, Specialization


# فیلد ورودی مشترک برای استایل یک‌دست تمام فرم‌ها
TEXT_WIDGET_CLASS = "form-control"


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
        }),
    )


# ---------------------------------------------------------------
# فرم‌های داشبورد مدیریتی (ورود اطلاعات هر بخش)
# ---------------------------------------------------------------

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "full_name", "membership_no", "license_no", "specializations",
            "photo", "phone", "email", "city", "address", "bio",
            "established_year", "status", "is_featured",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "membership_no": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "license_no": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "specializations": forms.SelectMultiple(attrs={"class": TEXT_WIDGET_CLASS}),
            "phone": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "email": forms.EmailInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "city": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "address": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "bio": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 4}),
            "established_year": forms.NumberInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "status": forms.Select(attrs={"class": TEXT_WIDGET_CLASS}),
        }


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ["title", "slug", "summary", "body", "cover_image", "is_published", "published_at"]
        widgets = {
            "title": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "slug": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "placeholder": "مثال: khabar-jadid"}),
            "summary": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "body": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 8}),
            "published_at": forms.DateTimeInput(attrs={"class": TEXT_WIDGET_CLASS, "type": "datetime-local"}),
        }


class CompletedWorkForm(forms.ModelForm):
    class Meta:
        model = CompletedWork
        fields = ["title", "member", "category", "description", "image", "completed_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "member": forms.Select(attrs={"class": TEXT_WIDGET_CLASS}),
            "category": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "description": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 5}),
            "completed_date": forms.DateInput(attrs={"class": TEXT_WIDGET_CLASS, "type": "date"}),
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


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ["title", "slug"]
        widgets = {
            "title": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "slug": forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS}),
        }
