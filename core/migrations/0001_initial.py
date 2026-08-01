import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DashboardAccess",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("permissions", models.JSONField(blank=True, default=dict, verbose_name="دسترسی‌ها")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="dashboard_access", to=settings.AUTH_USER_MODEL, verbose_name="کاربر")),
            ],
            options={
                "verbose_name": "دسترسی داشبورد",
                "verbose_name_plural": "دسترسی‌های داشبورد",
            },
        ),
    ]
