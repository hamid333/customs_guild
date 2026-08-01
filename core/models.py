"""
مدل‌های اپ core:
    DashboardAccess - تعیین می‌کند هر کاربر داشبورد در هر بخش، دقیقاً به کدام عملیات
                       (نمایش/افزودن/ویرایش/حذف) دسترسی دارد.

get_dashboard_sections() فهرست بخش‌های داشبورد را به‌صورت خودکار از روی اپ‌های نصب‌شده
می‌سازد: هر اپی که در AppConfig خودش «dashboard_section = True» را ست کرده باشد،
به‌طور خودکار یک بخش قابل‌دسترس در داشبورد محسوب می‌شود (اسلاگ = app_label، عنوان =
verbose_name همان اپ). یعنی برای افزودن اپ جدید به سیستم دسترسی‌ها، کافی است در
apps.py همان اپ این خط را اضافه کنید — نیازی به تغییر این فایل نیست.
"""
from django.apps import apps as django_apps
from django.conf import settings
from django.db import models

# چهار عملیات قابل‌کنترل روی هر بخش. ترتیب همان ترتیبی است که در جدول دسترسی‌ها نمایش داده می‌شود.
DASHBOARD_ACTIONS = [
    {"slug": "add", "label": "افزودن"},
    {"slug": "edit", "label": "ویرایش"},
    {"slug": "view", "label": "نمایش"},
    {"slug": "delete", "label": "حذف"},
]
DASHBOARD_ACTION_SLUGS = [a["slug"] for a in DASHBOARD_ACTIONS]


def get_dashboard_sections():
    """فهرست (اسلاگ, عنوان) بخش‌های داشبورد — به‌صورت خودکار از اپ‌های دارای
    dashboard_section=True در AppConfig، به‌علاوه‌ی بخش ثابت «مدیریت کاربران»."""
    sections = []
    for config in django_apps.get_app_configs():
        if getattr(config, "dashboard_section", False):
            sections.append((config.label, str(config.verbose_name)))
    sections.append(("users", "مدیریت کاربران"))
    return sections


class DashboardAccess(models.Model):
    """دسترسی هر کاربر به عملیات‌های هر بخش داشبورد. کاربران مدیر کل (superuser) صرف‌نظر
    از این مدل، همیشه به همه‌ی بخش‌ها و همه‌ی عملیات‌ها دسترسی دارند.

    ساختار permissions: {"<اسلاگ بخش>": ["view", "add", ...], ...}
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name="کاربر",
        on_delete=models.CASCADE, related_name="dashboard_access",
    )
    permissions = models.JSONField("دسترسی‌ها", default=dict, blank=True)

    class Meta:
        verbose_name = "دسترسی داشبورد"
        verbose_name_plural = "دسترسی‌های داشبورد"

    def __str__(self):
        return f"دسترسی‌های {self.user}"

    def has_permission(self, section, action):
        return action in (self.permissions.get(section) or [])

    def has_section(self, section):
        """آیا کاربر حداقل دسترسی «نمایش» به این بخش دارد؟ (برای نمایش/پنهان‌سازی لینک سایدبار)"""
        return self.has_permission(section, "view")

    def permission_summary(self):
        """برای نمایش در فهرست کاربران: «عنوان بخش (افزودن، ویرایش)» به ازای هر بخش."""
        section_labels = dict(get_dashboard_sections())
        action_labels = {a["slug"]: a["label"] for a in DASHBOARD_ACTIONS}
        result = []
        for slug, actions in (self.permissions or {}).items():
            if not actions:
                continue
            label = section_labels.get(slug, slug)
            actions_fa = "، ".join(action_labels.get(a, a) for a in actions)
            result.append(f"{label} ({actions_fa})")
        return result
