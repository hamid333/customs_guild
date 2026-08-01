from django.contrib import admin

from .models import DashboardAccess


@admin.register(DashboardAccess)
class DashboardAccessAdmin(admin.ModelAdmin):
    list_display = ("user", "permission_summary")
    search_fields = ("user__username",)
