from django.conf import settings


def site_info(request):
    """اطلاعات پایه‌ی سایت + فهرست زمینه‌های فعالیت (برای منوی کشویی) که در تمام قالب‌ها قابل استفاده است."""
    from specialization.models import Specialization  # ایمپورت داخل تابع برای جلوگیری از وابستگی حلقوی در زمان بارگذاری اپ‌ها

    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "انجمن صنفی حق‌العمل‌کاران گمرکی"),
        "SITE_PHONE": getattr(settings, "SITE_PHONE", ""),
        "SITE_EMAIL": getattr(settings, "SITE_EMAIL", ""),
        "SITE_ADDRESS": getattr(settings, "SITE_ADDRESS", ""),
        "nav_specializations": Specialization.objects.all()[:8],
    }
