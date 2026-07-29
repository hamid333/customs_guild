from django.contrib import admin
from .models import Specialization, Member, HSCode, NewsPost, CompletedWork, ContactMessage


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "membership_no", "city", "status", "is_featured", "created_at")
    list_filter = ("status", "is_featured", "specializations", "city")
    search_fields = ("full_name", "membership_no", "license_no", "email", "phone")
    filter_horizontal = ("specializations",)


@admin.register(HSCode)
class HSCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "title_fa", "category", "duty_rate")
    search_fields = ("code", "title_fa", "title_en", "category")
    list_filter = ("category",)


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at")
    list_filter = ("is_published",)
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(CompletedWork)
class CompletedWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "member", "category", "completed_date")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
