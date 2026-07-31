"""فرم‌های اپ core: ورود داشبورد + افزودن/ویرایش کاربر داشبورد (به‌همراه تعیین دسترسی بخش‌ها)."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import DASHBOARD_SECTIONS

User = get_user_model()

TEXT_WIDGET_CLASS = "form-control"


class StyledAuthenticationForm(AuthenticationForm):
    """فرم ورود داشبورد با کلاس‌های CSS یک‌دست با بقیه‌ی سایت."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": TEXT_WIDGET_CLASS, "placeholder": "نام کاربری"})
        self.fields["password"].widget.attrs.update({"class": TEXT_WIDGET_CLASS, "placeholder": "رمز عبور"})


class DashboardUserForm(forms.Form):
    """فرم افزودن/ویرایش کاربر داشبورد + تعیین دسترسی بخش‌ها (صفحه‌ی «کاربران» داشبورد)."""

    username = forms.CharField(
        label="نام کاربری", max_length=150,
        widget=forms.TextInput(attrs={"class": TEXT_WIDGET_CLASS, "autocomplete": "off"}),
    )
    email = forms.EmailField(
        label="ایمیل", required=False,
        widget=forms.EmailInput(attrs={"class": TEXT_WIDGET_CLASS}),
    )
    password = forms.CharField(
        label="رمز عبور", required=False,
        widget=forms.PasswordInput(attrs={
            "class": TEXT_WIDGET_CLASS,
            "placeholder": "برای کاربر جدید الزامی است؛ برای ویرایش خالی بگذارید تا تغییر نکند",
            "autocomplete": "new-password",
        }),
    )
    is_active = forms.BooleanField(label="حساب فعال باشد؟", required=False, initial=True)
    is_superuser = forms.BooleanField(
        label="مدیر کل (دسترسی کامل به همه‌ی بخش‌ها)", required=False,
        help_text="در صورت فعال بودن، انتخاب بخش‌های پایین دیگر تأثیری ندارد.",
    )
    sections = forms.MultipleChoiceField(
        label="بخش‌های قابل دسترس",
        required=False,
        choices=DASHBOARD_SECTIONS,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        super().__init__(*args, **kwargs)
        if instance is not None:
            self.fields["username"].initial = instance.username
            self.fields["email"].initial = instance.email
            self.fields["is_active"].initial = instance.is_active
            self.fields["is_superuser"].initial = instance.is_superuser
            access = getattr(instance, "dashboard_access", None)
            self.fields["sections"].initial = access.sections if access else []

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        qs = User.objects.filter(username=username)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("این نام کاربری قبلاً استفاده شده است.")
        return username

    def clean_password(self):
        pwd = self.cleaned_data.get("password", "")
        if self.instance is None and not pwd:
            raise forms.ValidationError("رمز عبور برای کاربر جدید الزامی است.")
        if pwd and len(pwd) < 6:
            raise forms.ValidationError("رمز عبور باید حداقل ۶ کاراکتر باشد.")
        return pwd

    def save(self):
        data = self.cleaned_data
        from .models import DashboardAccess  # جلوگیری از وابستگی حلقوی در بارگذاری ماژول

        if self.instance is not None:
            user = self.instance
            user.username = data["username"]
            user.email = data["email"]
            user.is_active = data["is_active"]
            user.is_superuser = data["is_superuser"]
            user.is_staff = True
            if data.get("password"):
                user.set_password(data["password"])
            user.save()
        else:
            user = User(
                username=data["username"], email=data["email"],
                is_active=data["is_active"], is_staff=True, is_superuser=data["is_superuser"],
            )
            user.set_password(data["password"])
            user.save()

        DashboardAccess.objects.update_or_create(user=user, defaults={"sections": data.get("sections", [])})
        return user
