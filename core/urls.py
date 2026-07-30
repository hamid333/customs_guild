"""
مسیرهای اصلی پروژه.
همه‌ی صفحات سایت داخل اپ portal تعریف شده‌اند.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("portal.urls", namespace="portal")),
]

# نمایش فایل‌های مدیا (تصاویر) در حالت توسعه (DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
