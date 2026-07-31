"""مدل ردیف تعرفه‌ی گمرکی (HS Code)."""
from django.db import models


class HSCode(models.Model):
    """ردیف تعرفه‌ی گمرکی (HS Code) برای بخش جست‌وجو."""

    code = models.CharField("کد تعرفه (HS Code)", max_length=20, db_index=True)
    title_fa = models.CharField("شرح کالا (فارسی)", max_length=300)
    title_en = models.CharField("شرح کالا (انگلیسی)", max_length=300, blank=True)
    category = models.CharField("گروه کالایی", max_length=150, blank=True)
    duty_rate = models.CharField("حقوق ورودی (سود بازرگانی)", max_length=30, blank=True,
                                  help_text="مثلاً 10٪ یا 4+10٪")
    notes = models.TextField("توضیحات / ضوابط", blank=True)

    class Meta:
        verbose_name = "ردیف تعرفه (HS Code)"
        verbose_name_plural = "ردیف‌های تعرفه (HS Code)"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.title_fa}"
