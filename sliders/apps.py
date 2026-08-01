from django.apps import AppConfig


class SlidersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sliders"
    verbose_name = "اسلایدر صفحه‌ی اصلی"
    dashboard_section = True  # این اپ به‌صورت خودکار یک بخش در داشبورد محسوب می‌شود
