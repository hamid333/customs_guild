from django.contrib import admin

import django_jalali.admin as jadmin  # noqa: F401
from django_jalali.admin.filters import JDateFieldListFilter

from .models import CompletedWork


@admin.register(CompletedWork)
class CompletedWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "member", "category", "completed_date")
    list_filter = ("category", ("completed_date", JDateFieldListFilter))
    search_fields = ("title", "description")
