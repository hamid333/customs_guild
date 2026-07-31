from django.contrib import admin

from .models import HeroSlide


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("__str__", "eyebrow", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
