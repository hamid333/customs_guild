"""
مسیرهای اصلی پروژه.
هر اپ مسئول بخش خودش است و URLهای خودش (هم عمومی و هم داشبورد همان بخش) را تعریف می‌کند.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("core.urls", namespace="core")),
    path("", include("specializations.urls", namespace="specializations")),
    path("", include("members.urls", namespace="members")),
    path("", include("hscodes.urls", namespace="hscodes")),
    path("", include("news.urls", namespace="news")),
    path("", include("works.urls", namespace="works")),
    path("", include("contact.urls", namespace="contact")),
    path("", include("sliders.urls", namespace="sliders")),
]

# نمایش فایل‌های مدیا (تصاویر) در حالت توسعه (DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
