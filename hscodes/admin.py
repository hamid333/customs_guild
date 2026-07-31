from django.contrib import admin

from .models import HSCode


@admin.register(HSCode)
class HSCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "title_fa", "category", "duty_rate")
    search_fields = ("code", "title_fa", "title_en", "category")
    list_filter = ("category",)
