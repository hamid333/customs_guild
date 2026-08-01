from django.apps import AppConfig


class SpecializationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "specializations"
    verbose_name = "زمینه‌های فعالیت"
    dashboard_section = True  # این اپ به‌صورت خودکار یک بخش در داشبورد محسوب می‌شود
