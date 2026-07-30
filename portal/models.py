import jdatetime
from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels

from member.models import Member

class HSCode(models.Model):
    """ردیف تعرفه‌ی گمرکی (HS Code) برای بخش جست‌وجو."""

    code = models.CharField("کد تعرفه (HS Code)", max_length=20, db_index=True)
    title_fa = models.CharField("شرح کالا (فارسی)", max_length=300)
    title_en = models.CharField("شرح کالا (انگلیسی)", max_length=300, blank=True)
    category = models.CharField("گروه کالایی", max_length=150, blank=True)
    duty_rate = models.CharField("حقوق ورودی (سود بازرگانی)", max_length=30, blank=True, help_text="مثلاً 10٪ یا 4+10٪")
    notes = models.TextField("توضیحات / ضوابط", blank=True)

    class Meta:
        verbose_name = "ردیف تعرفه (HS Code)"
        verbose_name_plural = "ردیف‌های تعرفه (HS Code)"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.title_fa}"


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
        return reverse("portal:news_detail", args=[self.slug])


class CompletedWork(models.Model):
    """نمونه‌کار / پرونده‌ی ترخیص انجام‌شده که به نمایش عمومی گذاشته می‌شود. تاریخ اتمام به‌صورت شمسی است."""

    title = models.CharField("عنوان پرونده / پروژه", max_length=250)
    member = models.ForeignKey(Member, verbose_name="عضو مجری", related_name="completed_works", on_delete=models.SET_NULL, blank=True, null=True)
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


class ContactMessage(models.Model):
    """پیام ارسالی از فرم «تماس با ما»."""

    name = models.CharField("نام و نام خانوادگی", max_length=150)
    email = models.EmailField("ایمیل")
    phone = models.CharField("تلفن", max_length=20, blank=True)
    subject = models.CharField("موضوع", max_length=200)
    message = models.TextField("متن پیام")
    created_at = models.DateTimeField("تاریخ ارسال", auto_now_add=True)
    is_read = models.BooleanField("خوانده‌شده", default=False)

    class Meta:
        verbose_name = "پیام تماس با ما"
        verbose_name_plural = "پیام‌های تماس با ما"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject}"


class HeroSlide(models.Model):
    """اسلاید اسلایدر صفحه‌ی اصلی. تمام فیلدها اختیاری هستند تا هر اسلاید بتواند
    ترکیب دلخواهی از تصویر، متن و دکمه داشته باشد."""

    eyebrow = models.CharField("عنوان کوچک (Eyebrow)", max_length=100, blank=True)
    title = models.CharField("تیتر اصلی", max_length=250, blank=True)
    description = models.TextField("متن توضیح", blank=True)
    image = models.ImageField("تصویر پس‌زمینه", upload_to="slides/", blank=True, null=True)
    button_text = models.CharField("متن دکمه", max_length=60, blank=True)
    button_url = models.CharField("لینک دکمه", max_length=300, blank=True,
                                   help_text="مثلاً /contact/ یا یک آدرس کامل https://...")
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("نمایش داده شود؟", default=True)

    class Meta:
        verbose_name = "اسلاید صفحه‌ی اصلی"
        verbose_name_plural = "اسلایدهای صفحه‌ی اصلی"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or f"اسلاید #{self.pk}"
