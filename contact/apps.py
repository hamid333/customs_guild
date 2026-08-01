from django.apps import AppConfig


class ContactConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contact"
    verbose_name = "تماس با ما"
    dashboard_section = True  # این اپ به‌صورت خودکار یک بخش در داشبورد محسوب می‌شود
