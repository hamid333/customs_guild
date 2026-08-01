from django.apps import AppConfig


class WorksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "works"
    verbose_name = "کارهای انجام‌شده"
    dashboard_section = True  # این اپ به‌صورت خودکار یک بخش در داشبورد محسوب می‌شود
