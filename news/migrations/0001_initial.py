import jdatetime
from django.db import migrations, models
import django_jalali.db.models as jmodels


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NewsPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250, verbose_name="عنوان خبر")),
                ("slug", models.SlugField(allow_unicode=True, max_length=270, unique=True, verbose_name="اسلاگ")),
                ("summary", models.CharField(max_length=400, verbose_name="خلاصه‌ی خبر")),
                ("body", models.TextField(verbose_name="متن کامل خبر")),
                ("cover_image", models.ImageField(blank=True, null=True, upload_to="news/", verbose_name="تصویر شاخص")),
                ("is_published", models.BooleanField(default=True, verbose_name="منتشر شود؟")),
                ("published_at", jmodels.jDateTimeField(default=jdatetime.datetime.now, verbose_name="تاریخ انتشار (شمسی)")),
            ],
            options={
                "verbose_name": "خبر",
                "verbose_name_plural": "اخبار",
                "ordering": ["-published_at"],
            },
        ),
    ]
