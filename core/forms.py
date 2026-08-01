"""فرم‌های اپ core: ورود داشبورد + افزودن/ویرایش کاربر داشبورد.

توجه: ماتریس دسترسی (بخش × عملیات) به‌صورت چک‌باکس‌های خام در قالب رندر می‌شود و در
ویو (core/views.py) به‌طور مستقیم از request.POST خوانده و در DashboardAccess ذخیره
می‌شود؛ چون شکل «ماتریسی» آن (بخش‌ها در سطر، عملیات‌ها در ستون) با فیلدهای استاندارد
فرم جنگو به‌سختی و با کد اضافه قابل نمایش است.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

TEXT_WIDGET_CLASS = "form-control"


class StyledAuthenticationForm(AuthenticationForm):
    """فرم ورود داشبورد با کلاس‌های CSS یک‌دست با بقیه‌ی سایت."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": TEXT_WIDGET_CLASS, "placeholder": "نام کاربری"})
        self.fields["password"].widget.attrs.update({"class": TEXT_WIDGET_CLASS, "placeholder": "رمز عبور"})


class DashboardUserForm(forms.Form):
    """فرم افزودن/ویرایش اطلاعات پایه‌ی کاربر داشبورد (ماتریس دسترسی جدا مدیریت می‌شود)."""

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
        label="مدیر کل (دسترسی کامل به همه‌ی بخش‌ها و عملیات‌ها)", required=False,
        help_text="در صورت فعال بودن، ماتریس دسترسی پایین دیگر تأثیری ندارد.",
    )

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        super().__init__(*args, **kwargs)
        if instance is not None:
            self.fields["username"].initial = instance.username
            self.fields["email"].initial = instance.email
            self.fields["is_active"].initial = instance.is_active
            self.fields["is_superuser"].initial = instance.is_superuser

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
        """فقط اطلاعات پایه‌ی کاربر (نه ماتریس دسترسی) را ذخیره و شیء User را برمی‌گرداند."""
        data = self.cleaned_data
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
        return user
