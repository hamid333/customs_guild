"""
مدل‌های اپ core:
    DashboardAccess - تعیین می‌کند هر کاربر داشبورد به کدام بخش‌ها دسترسی دارد.

DASHBOARD_SECTIONS فهرست ثابت بخش‌های داشبورد است (اسلاگ، عنوان فارسی) که هم در فرم
مدیریت کاربران و هم برای پنهان/نمایش کردن لینک‌های سایدبار استفاده می‌شود.
"""
from django.conf import settings
from django.db import models

DASHBOARD_SECTIONS = [
    ("members", "اعضای صنف"),
    ("specializations", "زمینه‌های فعالیت"),
    ("sliders", "اسلایدر صفحه‌ی اصلی"),
    ("news", "اخبار"),
    ("works", "کارهای انجام‌شده"),
    ("hscodes", "ردیف‌های تعرفه"),
    ("contact", "پیام‌های تماس"),
    ("users", "مدیریت کاربران"),
]


class DashboardAccess(models.Model):
    """دسترسی هر کاربر به بخش‌های مختلف داشبورد. کاربران مدیر کل (superuser) صرف‌نظر
    از این مدل، همیشه به همه‌ی بخش‌ها دسترسی دارند."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name="کاربر",
        on_delete=models.CASCADE, related_name="dashboard_access",
    )
    sections = models.JSONField("بخش‌های مجاز", default=list, blank=True)

    class Meta:
        verbose_name = "دسترسی داشبورد"
        verbose_name_plural = "دسترسی‌های داشبورد"

    def __str__(self):
        return f"دسترسی‌های {self.user}"

    def has_section(self, slug):
        return slug in (self.sections or [])

    def section_labels(self):
        mapping = dict(DASHBOARD_SECTIONS)
        return [mapping.get(s, s) for s in (self.sections or [])]
