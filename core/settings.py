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

    "django_jalali",

    # اپ اصلی سایت
    "portal",
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

ROOT_URLCONF = "core.urls"

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
                # پردازشگر سفارشی برای در دسترس بودن اطلاعات پایه‌ی سایت در همه‌ی قالب‌ها
                "portal.context_processors.site_info",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

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
STATICFILES_DIRS = [BASE_DIR / "portal" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # برای collectstatic در production

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"  # تصاویر اعضا، نمونه‌کارها و اخبار اینجا ذخیره می‌شوند

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------
# ورود/خروج داشبورد
# ------------------------------------------------------------------
LOGIN_URL = "portal:dashboard_login"
LOGIN_REDIRECT_URL = "portal:dashboard_home"
LOGOUT_REDIRECT_URL = "portal:home"

# اطلاعات پایه‌ی سایت (نام انجمن، اطلاعات تماس) که در context_processors استفاده می‌شود
SITE_NAME = "انجمن صنفی حق‌العمل‌کاران گمرکی"
SITE_PHONE = "021-88112233"
SITE_EMAIL = "info@customs-guild.example"
SITE_ADDRESS = "تهران، خیابان گمرک، ساختمان مرکزی انجمن، طبقه‌ی سوم"
