from django.contrib import admin

from .models import DashboardAccess


@admin.register(DashboardAccess)
class DashboardAccessAdmin(admin.ModelAdmin):
    list_display = ("user", "section_labels")
    search_fields = ("user__username",)
