from django.contrib import admin

from .models import (Specialization)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)

