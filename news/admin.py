from django.contrib import admin

# ایمپورت زیر طبق مستندات django-jalali لازم است تا فیلدهای jDateField/jDateTimeField
# در پنل ادمین با ویجت تقویم شمسی نمایش داده شوند.
import django_jalali.admin as jadmin  # noqa: F401
from django_jalali.admin.filters import JDateFieldListFilter

from .models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at")
    list_filter = ("is_published", ("published_at", JDateFieldListFilter))
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
