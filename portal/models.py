"""
مدل‌های داده‌ای سایت انجمن صنفی حق‌العمل‌کاران گمرکی.

مدل‌ها:
    Specialization   - زمینه‌ی فعالیت/تخصص (مثلاً «ترخیص خودرو»، «صادرات») — قابل افزودن دستی از داشبورد
    Member           - عضو صنف (حق‌العمل‌کار گمرکی)
    HSCode           - ردیف تعرفه‌ی گمرکی برای جست‌وجو
    NewsPost         - خبر/مقاله‌ی سایت (تاریخ انتشار به‌صورت شمسی)
    CompletedWork    - نمونه‌کار / پرونده‌ی انجام‌شده (تاریخ اتمام به‌صورت شمسی)
    ContactMessage   - پیام‌های فرم تماس با ما
    HeroSlide        - اسلایدهای اسلایدر صفحه‌ی اصلی (تمام فیلدها اختیاری)

نکته: تاریخ‌هایی که باید توسط کاربر وارد شوند (تاریخ اتمام کار، تاریخ انتشار خبر)
از نوع jDateField/jDateTimeField کتابخانه‌ی django-jalali هستند تا ورود/نمایش
به‌صورت تاریخ شمسی (جلالی) انجام شود. تاریخ‌های خودکار سیستمی (مثل تاریخ ثبت رکورد)
همچنان میلادی (DateTimeField معمولی) باقی مانده‌اند.
"""
import jdatetime
from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels


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


class Member(models.Model):
    """عضو صنف حق‌العمل‌کاران گمرکی (شرکت یا نماینده‌ی حقیقی)."""

    STATUS_ACTIVE = "active"
    STATUS_SUSPENDED = "suspended"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "فعال"),
        (STATUS_SUSPENDED, "تعلیق‌شده"),
    ]

    ROLE_NORMAL = "normal"
    ROLE_CEO = "ceo"
    ROLE_INSPECTOR = "inspector"
    ROLE_OTHER = "other"
    ROLE_CHOICES = [
        (ROLE_NORMAL, "کاربر عادی"),
        (ROLE_CEO, "مدیرعامل"),
        (ROLE_INSPECTOR, "بازرس"),
        (ROLE_OTHER, "شخص دیگر"),
    ]

    full_name = models.CharField("نام و نام خانوادگی / نام شرکت", max_length=200)
    membership_no = models.CharField("شماره‌ی عضویت", max_length=30, unique=True)
    license_no = models.CharField("شماره‌ی پروانه‌ی گمرکی", max_length=30, blank=True)
    role = models.CharField("سمت / نوع عضویت", max_length=12, choices=ROLE_CHOICES, default=ROLE_NORMAL)
    specializations = models.ManyToManyField(
        Specialization, verbose_name="زمینه‌های فعالیت", related_name="members", blank=True
    )
    photo = models.ImageField("تصویر / لوگو", upload_to="members/", blank=True, null=True)
    phone = models.CharField("تلفن تماس", max_length=20, blank=True)
    email = models.EmailField("ایمیل", blank=True)
    city = models.CharField("شهر", max_length=80, blank=True)
    address = models.CharField("آدرس دفتر", max_length=300, blank=True)
    bio = models.TextField("درباره / سوابق فعالیت", blank=True)
    established_year = models.PositiveIntegerField("سال شروع فعالیت", blank=True, null=True)
    status = models.CharField("وضعیت عضویت", max_length=12, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    is_featured = models.BooleanField("نمایش در صفحه‌ی اصلی / اعضای اصلی", default=False)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "عضو صنف"
        verbose_name_plural = "اعضای صنف"
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.membership_no})"

    def get_absolute_url(self):
        return reverse("portal:member_detail", args=[self.pk])


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
