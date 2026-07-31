"""پردازشگرهای context مشترک که در تمام قالب‌های سایت در دسترس‌اند."""
from django.conf import settings

from .models import DASHBOARD_SECTIONS


def site_info(request):
    """اطلاعات پایه‌ی سایت + فهرست زمینه‌های فعالیت (برای منوی کشویی)."""
    from specializations.models import Specialization  # ایمپورت داخل تابع برای جلوگیری از وابستگی حلقوی بین اپ‌ها

    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "انجمن صنفی حق‌العمل‌کاران گمرکی"),
        "SITE_PHONE": getattr(settings, "SITE_PHONE", ""),
        "SITE_EMAIL": getattr(settings, "SITE_EMAIL", ""),
        "SITE_ADDRESS": getattr(settings, "SITE_ADDRESS", ""),
        "nav_specializations": Specialization.objects.all()[:8],
    }


def dashboard_sections(request):
    """اسلاگ بخش‌های داشبورد که کاربر جاری به آن‌ها دسترسی دارد (برای نمایش/پنهان‌سازی
    لینک‌های سایدبار داشبورد). برای کاربران غیر staff همیشه خالی است."""
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated or not user.is_staff:
        return {"user_dashboard_sections": set()}
    if user.is_superuser:
        return {"user_dashboard_sections": {slug for slug, _ in DASHBOARD_SECTIONS}}
    access = getattr(user, "dashboard_access", None)
    return {"user_dashboard_sections": set(access.sections) if access else set()}
