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

from .models import (Member)

# کلاس‌های CSS مشترک برای یک‌دستی ظاهر فرم‌ها
TEXT_WIDGET_CLASS = "form-control"
SELECT2_WIDGET_CLASS = "form-control select2-field"
JALALI_DATE_CLASS = "form-control jalali-datepicker"
JALALI_DATETIME_CLASS = "form-control jalali-datetimepicker"


# ---------------------------------------------------------------
# فرم‌های داشبورد مدیریتی (ورود اطلاعات هر بخش)
# ---------------------------------------------------------------

class MemberForm(forms.ModelForm):
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
            "bio": forms.Textarea(attrs={"class": TEXT_WIDGET_CLASS, "rows": 4}),
            "established_year": forms.NumberInput(attrs={"class": TEXT_WIDGET_CLASS}),
            "status": forms.Select(attrs={"class": SELECT2_WIDGET_CLASS}),
        }


