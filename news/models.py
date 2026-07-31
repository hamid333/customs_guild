"""مدل خبر (NewsPost). تاریخ انتشار به‌صورت شمسی است."""
import jdatetime
from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels


class NewsPost(models.Model):
    """خبر یا اطلاعیه‌ی انجمن. تاریخ انتشار به‌صورت شمسی وارد می‌شود."""

    title = models.CharField("عنوان خبر", max_length=250)
    slug = models.SlugField("اسلاگ", max_length=270, unique=True, allow_unicode=True)
    summary = models.CharField("خلاصه‌ی خبر", max_length=400)
    body = models.TextField("متن کامل خبر")
    cover_image = models.ImageField("تصویر شاخص", upload_to="news/", blank=True, null=True)
    is_published = models.BooleanField("منتشر شود؟", default=True)
    published_at = jmodels.jDateTimeField("تاریخ انتشار (شمسی)", default=jdatetime.datetime.now)

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:news_detail", args=[self.slug])
