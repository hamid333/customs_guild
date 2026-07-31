import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ("specializations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=200, verbose_name="نام و نام خانوادگی / نام شرکت")),
                ("membership_no", models.CharField(max_length=30, unique=True, verbose_name="شماره‌ی عضویت")),
                ("license_no", models.CharField(blank=True, max_length=30, verbose_name="شماره‌ی پروانه‌ی گمرکی")),
                ("role", models.CharField(choices=[("normal", "کاربر عادی"), ("ceo", "مدیرعامل"), ("inspector", "بازرس"), ("other", "شخص دیگر")], default="normal", max_length=12, verbose_name="سمت / نوع عضویت")),
                ("photo", models.ImageField(blank=True, null=True, upload_to="members/", verbose_name="تصویر / لوگو")),
                ("phone", models.CharField(blank=True, max_length=20, verbose_name="تلفن تماس")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="ایمیل")),
                ("city", models.CharField(blank=True, max_length=80, verbose_name="شهر")),
                ("address", models.CharField(blank=True, max_length=300, verbose_name="آدرس دفتر")),
                ("bio", models.TextField(blank=True, verbose_name="درباره / سوابق فعالیت")),
                ("established_year", models.PositiveIntegerField(blank=True, null=True, verbose_name="سال شروع فعالیت")),
                ("status", models.CharField(choices=[("active", "فعال"), ("suspended", "تعلیق‌شده")], default="active", max_length=12, verbose_name="وضعیت عضویت")),
                ("is_featured", models.BooleanField(default=False, verbose_name="نمایش در صفحه‌ی اصلی / اعضای اصلی")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")),
                ("specializations", models.ManyToManyField(blank=True, related_name="members", to="specializations.specialization", verbose_name="زمینه‌های فعالیت")),
            ],
            options={
                "verbose_name": "عضو صنف",
                "verbose_name_plural": "اعضای صنف",
                "ordering": ["full_name"],
            },
        ),
    ]
