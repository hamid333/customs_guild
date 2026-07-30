import django.db.models.deletion
import jdatetime
from django.db import migrations, models
import django_jalali.db.models as jmodels


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="role",
            field=models.CharField(
                choices=[
                    ("normal", "کاربر عادی"),
                    ("ceo", "مدیرعامل"),
                    ("inspector", "بازرس"),
                    ("other", "شخص دیگر"),
                ],
                default="normal",
                max_length=12,
                verbose_name="سمت / نوع عضویت",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="is_featured",
            field=models.BooleanField(default=False, verbose_name="نمایش در صفحه‌ی اصلی / اعضای اصلی"),
        ),
        migrations.AlterField(
            model_name="newspost",
            name="published_at",
            field=jmodels.jDateTimeField(default=jdatetime.datetime.now, verbose_name="تاریخ انتشار (شمسی)"),
        ),
        migrations.AlterField(
            model_name="completedwork",
            name="completed_date",
            field=jmodels.jDateField(default=jdatetime.date.today, verbose_name="تاریخ اتمام کار (شمسی)"),
        ),
        migrations.CreateModel(
            name="HeroSlide",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("eyebrow", models.CharField(blank=True, max_length=100, verbose_name="عنوان کوچک (Eyebrow)")),
                ("title", models.CharField(blank=True, max_length=250, verbose_name="تیتر اصلی")),
                ("description", models.TextField(blank=True, verbose_name="متن توضیح")),
                ("image", models.ImageField(blank=True, null=True, upload_to="slides/", verbose_name="تصویر پس‌زمینه")),
                ("button_text", models.CharField(blank=True, max_length=60, verbose_name="متن دکمه")),
                ("button_url", models.CharField(blank=True, help_text="مثلاً /contact/ یا یک آدرس کامل https://...", max_length=300, verbose_name="لینک دکمه")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")),
                ("is_active", models.BooleanField(default=True, verbose_name="نمایش داده شود؟")),
            ],
            options={
                "verbose_name": "اسلاید صفحه‌ی اصلی",
                "verbose_name_plural": "اسلایدهای صفحه‌ی اصلی",
                "ordering": ["order", "id"],
            },
        ),
    ]
