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
    ]
