import django.db.models.deletion
import jdatetime
from django.db import migrations, models
import django_jalali.db.models as jmodels


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ("members", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompletedWork",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250, verbose_name="عنوان پرونده / پروژه")),
                ("category", models.CharField(blank=True, max_length=150, verbose_name="دسته‌بندی")),
                ("description", models.TextField(verbose_name="شرح کار انجام‌شده")),
                ("image", models.ImageField(blank=True, null=True, upload_to="works/", verbose_name="تصویر")),
                ("completed_date", jmodels.jDateField(default=jdatetime.date.today, verbose_name="تاریخ اتمام کار (شمسی)")),
                ("member", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="completed_works", to="members.member", verbose_name="عضو مجری")),
            ],
            options={
                "verbose_name": "نمونه‌کار انجام‌شده",
                "verbose_name_plural": "نمونه‌کارهای انجام‌شده",
                "ordering": ["-completed_date"],
            },
        ),
    ]
