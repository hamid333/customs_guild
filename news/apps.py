from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"
    verbose_name = "اخبار"
    dashboard_section = True  # این اپ به‌صورت خودکار یک بخش در داشبورد محسوب می‌شود
