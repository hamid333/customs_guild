from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "membership_no", "role", "city", "status", "is_featured", "created_at")
    list_filter = ("status", "role", "is_featured", "specializations", "city")
    search_fields = ("full_name", "membership_no", "license_no", "email", "phone")
    filter_horizontal = ("specializations",)
