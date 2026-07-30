from django.db import models


class Specialization(models.Model):
    """زمینه‌ی فعالیت اعضا؛ مثال: ترخیص کالای صنعتی، واردات خودرو، صادرات، امور بنادر.
    از داشبورد مدیریتی قابل افزودن/ویرایش/حذف دستی است."""

    title = models.CharField("عنوان زمینه‌ی فعالیت", max_length=150, unique=True)
    slug = models.SlugField("اسلاگ", max_length=170, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "زمینه‌ی فعالیت"
        verbose_name_plural = "زمینه‌های فعالیت"
        ordering = ["title"]

    def __str__(self):
        return self.title
