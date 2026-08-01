"""
تنظیمات پروژه‌ی جنگو برای «انجمن صنفی حق‌العمل‌کاران گمرکی»
Settings for the Customs Brokers Guild (انجمن حق‌العمل‌کاران گمرکی) website.

این فایل با دست و متناسب با Django 4.2 نوشته شده است.
برای اجرا: نگاه کنید به README.md در ریشه‌ی پروژه.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# امنیت / Security
# ------------------------------------------------------------------
# هشدار: این کلید فقط برای توسعه (development) است.
# پیش از انتشار در محیط production حتماً آن را با یک مقدار تصادفی و محرمانه جایگزین کنید
# (مثلاً با: python -c "import secrets; print(secrets.token_urlsafe(50))")
SECRET_KEY = "django-insecure-CHANGE-THIS-KEY-BEFORE-DEPLOYMENT-!!!"

# در محیط تولید (production) حتماً DEBUG = False کنید.
DEBUG = True

ALLOWED_HOSTS = ["*"]  # در production این را به دامنه‌ی واقعی محدود کنید

# ------------------------------------------------------------------
# اپلیکیشن‌های نصب‌شده
# ------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # برای نمایش بهتر تاریخ/اعداد در قالب‌ها

    "django_jalali",  # پشتیبانی از تاریخ شمسی (jDateField / jDateTimeField) + ویجت‌های ادمین
    "ckeditor",        # ویرایشگر متن غنی (Rich Text) — برای سوابق فعالیت اعضا

    # اپ‌های سایت — هرکدام مسئول یک بخش مستقل هستند
    "core",              # صفحه‌ی اصلی، ورود/خروج داشبورد، مدیریت کاربران و دسترسی‌ها
    "specializations",   # زمینه‌های فعالیت
    "members",            # اعضای صنف (به specializations وابسته است)
    "hscodes",             # ردیف‌های تعرفه (HS Code)
    "news",                 # اخبار
    "works",                 # کارهای انجام‌شده (به members وابسته است)
    "contact",                # پیام‌های تماس با ما
    "sliders",                 # اسلایدهای صفحه‌ی اصلی
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "customs_guild.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # پردازشگرهای سفارشی: اطلاعات پایه‌ی سایت + دسترسی بخش‌های داشبورد
                "core.context_processors.site_info",
                "core.context_processors.dashboard_sections",
            ],
        },
    },
]

WSGI_APPLICATION = "customs_guild.wsgi.application"
ASGI_APPLICATION = "customs_guild.asgi.application"

# ------------------------------------------------------------------
# پایگاه داده / Database
# برای سادگی از SQLite استفاده شده؛ برای production می‌توانید به PostgreSQL سوییچ کنید.
# ------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'customs_guild',
        'USER': 'postgres',
        'PASSWORD': 'H@m!dS!m@',
    }
}

# ------------------------------------------------------------------
# اعتبارسنجی رمز عبور
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------
# بین‌المللی‌سازی / زبان و راست‌به‌چپ بودن
# ------------------------------------------------------------------
LANGUAGE_CODE = "fa"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# فایل‌های استاتیک و مدیا
# ------------------------------------------------------------------
STATIC_URL = "static/"
# توجه: فایل‌های استاتیک اکنون داخل core/static/core/ قرار دارند و توسط
# AppDirectoriesFinder پیش‌فرض جنگو به‌صورت خودکار پیدا می‌شوند (نیازی به STATICFILES_DIRS نیست).
STATIC_ROOT = BASE_DIR / "staticfiles"  # برای collectstatic در production

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"  # تصاویر اعضا، نمونه‌کارها و اخبار اینجا ذخیره می‌شوند

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------
# ورود/خروج داشبورد
# ------------------------------------------------------------------
LOGIN_URL = "core:dashboard_login"
LOGIN_REDIRECT_URL = "core:dashboard_home"
LOGOUT_REDIRECT_URL = "core:home"

# اطلاعات پایه‌ی سایت (نام انجمن، اطلاعات تماس) که در context_processors استفاده می‌شود
SITE_NAME = "انجمن صنفی حق‌العمل‌کاران گمرکی"
SITE_PHONE = "021-88112233"
SITE_EMAIL = "info@customs-guild.example"
SITE_ADDRESS = "تهران، خیابان گمرک، ساختمان مرکزی انجمن، طبقه‌ی سوم"

# ------------------------------------------------------------------
# CKEditor — برای ویرایش زیبا و غنی (Rich Text) سوابق فعالیت اعضا (Member.bio)
# ------------------------------------------------------------------
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Format"],
            ["Bold", "Italic", "Underline", "Strike"],
            ["TextColor", "BGColor"],
            ["NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Blockquote"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight"],
            ["Link", "Unlink"],
            ["Image", "Table", "HorizontalRule"],
            ["Undo", "Redo"],
            ["Source"],
        ],
        "height": 260,
        "width": "100%",
        # پشتیبانی از راست‌به‌چپ برای محتوای فارسی
        "language": "fa",
        "contentsLangDirection": "rtl",
    },
}

