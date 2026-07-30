from django.db import models


class HeroSlide(models.Model):
    """اسلاید اسلایدر صفحه‌ی اصلی. تمام فیلدها اختیاری هستند تا هر اسلاید بتواند
    ترکیب دلخواهی از تصویر، متن و دکمه داشته باشد."""

    eyebrow = models.CharField("عنوان کوچک (Eyebrow)", max_length=100, blank=True)
    title = models.CharField("تیتر اصلی", max_length=250, blank=True)
    description = models.TextField("متن توضیح", blank=True)
    image = models.ImageField("تصویر پس‌زمینه", upload_to="slides/", blank=True, null=True)
    button_text = models.CharField("متن دکمه", max_length=60, blank=True)
    button_url = models.CharField("لینک دکمه", max_length=300, blank=True,help_text="مثلاً /contact/ یا یک آدرس کامل https://...")
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("نمایش داده شود؟", default=True)

    class Meta:
        verbose_name = "اسلاید صفحه‌ی اصلی"
        verbose_name_plural = "اسلایدهای صفحه‌ی اصلی"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or f"اسلاید #{self.pk}"

