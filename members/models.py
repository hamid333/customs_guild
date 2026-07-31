"""مدل عضو صنف (Member)."""
from django.db import models
from django.urls import reverse

from specializations.models import Specialization


class Member(models.Model):
    """عضو صنف حق‌العمل‌کاران گمرکی (شرکت یا نماینده‌ی حقیقی)."""

    STATUS_ACTIVE = "active"
    STATUS_SUSPENDED = "suspended"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "فعال"),
        (STATUS_SUSPENDED, "تعلیق‌شده"),
    ]

    ROLE_NORMAL = "normal"
    ROLE_CEO = "ceo"
    ROLE_INSPECTOR = "inspector"
    ROLE_OTHER = "other"
    ROLE_CHOICES = [
        (ROLE_NORMAL, "کاربر عادی"),
        (ROLE_CEO, "مدیرعامل"),
        (ROLE_INSPECTOR, "بازرس"),
        (ROLE_OTHER, "شخص دیگر"),
    ]

    full_name = models.CharField("نام و نام خانوادگی / نام شرکت", max_length=200)
    membership_no = models.CharField("شماره‌ی عضویت", max_length=30, unique=True)
    license_no = models.CharField("شماره‌ی پروانه‌ی گمرکی", max_length=30, blank=True)
    role = models.CharField("سمت / نوع عضویت", max_length=12, choices=ROLE_CHOICES, default=ROLE_NORMAL)
    specializations = models.ManyToManyField(
        Specialization, verbose_name="زمینه‌های فعالیت", related_name="members", blank=True
    )
    photo = models.ImageField("تصویر / لوگو", upload_to="members/", blank=True, null=True)
    phone = models.CharField("تلفن تماس", max_length=20, blank=True)
    email = models.EmailField("ایمیل", blank=True)
    city = models.CharField("شهر", max_length=80, blank=True)
    address = models.CharField("آدرس دفتر", max_length=300, blank=True)
    bio = models.TextField("درباره / سوابق فعالیت", blank=True)
    established_year = models.PositiveIntegerField("سال شروع فعالیت", blank=True, null=True)
    status = models.CharField("وضعیت عضویت", max_length=12, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    is_featured = models.BooleanField("نمایش در صفحه‌ی اصلی / اعضای اصلی", default=False)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "عضو صنف"
        verbose_name_plural = "اعضای صنف"
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.membership_no})"

    def get_absolute_url(self):
        return reverse("members:member_detail", args=[self.pk])
