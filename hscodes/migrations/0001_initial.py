from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
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
    ]
