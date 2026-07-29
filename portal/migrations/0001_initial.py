import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Specialization",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150, unique=True, verbose_name="عنوان زمینه‌ی فعالیت")),
                ("slug", models.SlugField(allow_unicode=True, max_length=170, unique=True, verbose_name="اسلاگ")),
            ],
            options={
                "verbose_name": "زمینه‌ی فعالیت",
                "verbose_name_plural": "زمینه‌های فعالیت",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="HSCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(db_index=True, max_length=20, verbose_name="کد تعرفه (HS Code)")),
                ("title_fa", models.CharField(max_length=300, verbose_name="شرح کالا (فارسی)")),
                ("title_en", models.CharField(blank=True, max_length=300, verbose_name="شرح کالا (انگلیسی)")),
                ("category", models.CharField(blank=True, max_length=150, verbose_name="گروه کالایی")),
                ("duty_rate", models.CharField(blank=True, help_text="مثلاً 10٪ یا 4+10٪", max_length=30, verbose_name="حقوق ورودی (سود بازرگانی)")),
                ("notes", models.TextField(blank=True, verbose_name="توضیحات / ضوابط")),
            ],
            options={
                "verbose_name": "ردیف تعرفه (HS Code)",
                "verbose_name_plural": "ردیف‌های تعرفه (HS Code)",
                "ordering": ["code"],
            },
        ),
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
                ("published_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="تاریخ انتشار")),
            ],
            options={
                "verbose_name": "خبر",
                "verbose_name_plural": "اخبار",
                "ordering": ["-published_at"],
            },
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=200, verbose_name="نام و نام خانوادگی / نام شرکت")),
                ("membership_no", models.CharField(max_length=30, unique=True, verbose_name="شماره‌ی عضویت")),
                ("license_no", models.CharField(blank=True, max_length=30, verbose_name="شماره‌ی پروانه‌ی گمرکی")),
                ("photo", models.ImageField(blank=True, null=True, upload_to="members/", verbose_name="تصویر / لوگو")),
                ("phone", models.CharField(blank=True, max_length=20, verbose_name="تلفن تماس")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="ایمیل")),
                ("city", models.CharField(blank=True, max_length=80, verbose_name="شهر")),
                ("address", models.CharField(blank=True, max_length=300, verbose_name="آدرس دفتر")),
                ("bio", models.TextField(blank=True, verbose_name="درباره / سوابق فعالیت")),
                ("established_year", models.PositiveIntegerField(blank=True, null=True, verbose_name="سال شروع فعالیت")),
                ("status", models.CharField(choices=[("active", "فعال"), ("suspended", "تعلیق‌شده")], default="active", max_length=12, verbose_name="وضعیت عضویت")),
                ("is_featured", models.BooleanField(default=False, verbose_name="نمایش در صفحه‌ی اصلی")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")),
                ("specializations", models.ManyToManyField(blank=True, related_name="members", to="portal.specialization", verbose_name="زمینه‌های فعالیت")),
            ],
            options={
                "verbose_name": "عضو صنف",
                "verbose_name_plural": "اعضای صنف",
                "ordering": ["full_name"],
            },
        ),
        migrations.CreateModel(
            name="CompletedWork",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250, verbose_name="عنوان پرونده / پروژه")),
                ("category", models.CharField(blank=True, max_length=150, verbose_name="دسته‌بندی")),
                ("description", models.TextField(verbose_name="شرح کار انجام‌شده")),
                ("image", models.ImageField(blank=True, null=True, upload_to="works/", verbose_name="تصویر")),
                ("completed_date", models.DateField(default=django.utils.timezone.now, verbose_name="تاریخ اتمام کار")),
                ("member", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="completed_works", to="portal.member", verbose_name="عضو مجری")),
            ],
            options={
                "verbose_name": "نمونه‌کار انجام‌شده",
                "verbose_name_plural": "نمونه‌کارهای انجام‌شده",
                "ordering": ["-completed_date"],
            },
        ),
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
