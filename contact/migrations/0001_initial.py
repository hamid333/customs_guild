from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")),
                ("email", models.EmailField(max_length=254, verbose_name="ایمیل")),
                ("phone", models.CharField(blank=True, max_length=20, verbose_name="تلفن")),
                ("subject", models.CharField(max_length=200, verbose_name="موضوع")),
                ("message", models.TextField(verbose_name="متن پیام")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")),
                ("is_read", models.BooleanField(default=False, verbose_name="خوانده‌شده")),
            ],
            options={
                "verbose_name": "پیام تماس با ما",
                "verbose_name_plural": "پیام‌های تماس با ما",
                "ordering": ["-created_at"],
            },
        ),
    ]
