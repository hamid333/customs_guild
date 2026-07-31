"""مدل نمونه‌کار (CompletedWork). تاریخ اتمام به‌صورت شمسی است."""
import jdatetime
from django.db import models
from django_jalali.db import models as jmodels

from members.models import Member


class CompletedWork(models.Model):
    """نمونه‌کار / پرونده‌ی ترخیص انجام‌شده که به نمایش عمومی گذاشته می‌شود. تاریخ اتمام به‌صورت شمسی است."""

    title = models.CharField("عنوان پرونده / پروژه", max_length=250)
    member = models.ForeignKey(
        Member, verbose_name="عضو مجری", related_name="completed_works",
        on_delete=models.SET_NULL, blank=True, null=True
    )
    category = models.CharField("دسته‌بندی", max_length=150, blank=True)
    description = models.TextField("شرح کار انجام‌شده")
    image = models.ImageField("تصویر", upload_to="works/", blank=True, null=True)
    completed_date = jmodels.jDateField("تاریخ اتمام کار (شمسی)", default=jdatetime.date.today)

    class Meta:
        verbose_name = "نمونه‌کار انجام‌شده"
        verbose_name_plural = "نمونه‌کارهای انجام‌شده"
        ordering = ["-completed_date"]

    def __str__(self):
        return self.title
