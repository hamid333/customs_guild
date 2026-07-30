# سایت انجمن صنفی حق‌العمل‌کاران گمرکی (Django)

پروژه‌ای کامل با جنگو برای انجمن صنفی حق‌العمل‌کاران گمرکی، شامل:

- صفحه‌ی اصلی با اسلایدر تمام‌صفحه که کاملاً از داشبورد قابل مدیریت است (هر اسلاید: عنوان کوچک/تیتر/توضیح/تصویر/دکمه — همه اختیاری)
- صفحه‌ی «اعضای اصلی» (اعضای معرفی‌شده) و صفحه‌ی «همه‌ی اعضا» (با جست‌وجو و فیلتر بر اساس زمینه‌ی فعالیت)
- هر عضو دارای سمت مشخص است: کاربر عادی، مدیرعامل، بازرس یا شخص دیگر
- صفحه‌ی جست‌وجوی ردیف تعرفه‌ی گمرکی (HS Code)
- صفحه‌ی اخبار سایت (+ نوار اخبار فوری) — تاریخ انتشار به‌صورت شمسی
- صفحه‌ی کارهای انجام‌شده (نمونه‌کارها) — تاریخ اتمام به‌صورت شمسی
- صفحه‌ی تماس با ما
- مدل «زمینه‌ی فعالیت» (Specialization) که هم از پنل ادمین و هم از داشبورد قابل افزودن دستی است
- داشبورد مدیریتی حرفه‌ای با بخش جداگانه برای هر قسمت (اعضا، زمینه‌های فعالیت، اسلایدر، اخبار، نمونه‌کارها، ردیف‌های تعرفه، پیام‌های تماس)
- **افزودن/ویرایش/حذف همه‌ی بخش‌های داشبورد از طریق مودال SweetAlert2** (بدون نیاز به رفتن به صفحه‌ی جداگانه)
- انتخاب‌گرهای چندگزینه‌ای و لیست‌های بلند با **Select2** (جست‌وجوپذیر و RTL)
- ورود تاریخ (تاریخ اتمام کار، تاریخ انتشار خبر) با **تقویم شمسی** از طریق کتابخانه‌ی `django-jalali` + `persian-datepicker`
- پنل ادمین جنگو (`/admin/`) به‌عنوان مسیر مدیریتی جایگزین/مکمل (با ویجت تقویم شمسی)

هویت بصری: رنگ اصلی سورمه‌ای (`#0b1a2e`)، رنگ مکمل طلایی کهنه (`#c9a94e`) و مسی (`#b87333`).

## پیش‌نیازها

- Python 3.10 یا بالاتر
- pip
- **اتصال اینترنت در مرورگر** برای بارگذاری کتابخانه‌های CDN داشبورد: jQuery، Select2،
  SweetAlert2 و persian-datepicker (این‌ها از CDN بارگذاری می‌شوند و در پروژه باندل نشده‌اند).
  اگر سرور شما به اینترنت خارجی دسترسی ندارد، این فایل‌ها را دانلود و در `portal/static/portal/vendor/`
  قرار دهید و لینک‌های CDN را در `portal/templates/portal/dashboard/base_dashboard.html` به مسیر محلی تغییر دهید.

## نصب و اجرا (محیط توسعه)

```bash
# 1) ساخت و فعال‌سازی محیط مجازی
python3 -m venv .venv
source .venv/bin/activate        # ویندوز: .venv\Scripts\activate

# 2) نصب وابستگی‌ها (شامل django-jalali و Pillow)
pip install -r requirements.txt

# 3) اجرای مایگریشن‌ها (ساخت پایگاه‌داده‌ی SQLite)
python manage.py migrate

# 4) ساخت کاربر مدیر برای ورود به داشبورد و پنل ادمین
python manage.py createsuperuser

# 5) (اختیاری اما پیشنهادی) پرکردن پایگاه‌داده با داده‌ی نمونه برای تست سریع
python manage.py seed_data

# 6) اجرای سرور توسعه
python manage.py runserver
```

سپس:
- سایت عمومی: http://127.0.0.1:8000/
- اعضای اصلی: http://127.0.0.1:8000/members/featured/
- داشبورد مدیریتی: http://127.0.0.1:8000/dashboard/login/
- پنل ادمین جنگو: http://127.0.0.1:8000/admin/

برای ورود به داشبورد، کاربر باید `is_staff=True` باشد (کاربر ساخته‌شده با `createsuperuser` به‌صورت پیش‌فرض staff است).

## نحوه‌ی کار مودال‌های افزودن/ویرایش/حذف (SweetAlert2)

هر دکمه‌ی «افزودن»/«ویرایش» در داشبورد یک `data-modal-form` با `data-url` به آدرس ثبت/ویرایش دارد.
با کلیک روی آن، `static/portal/js/dashboard.js` فرم را به‌صورت AJAX از همان ویو جنگو می‌گیرد و
داخل یک مودال SweetAlert2 نمایش می‌دهد؛ ثبت فرم هم از طریق همان مودال و AJAX انجام می‌شود.
دکمه‌های «حذف» هم با `data-modal-delete` یک تأییدیه‌ی SweetAlert2 نشان می‌دهند و در صورت تأیید،
درخواست حذف را ارسال می‌کنند. تمام ویوهای Create/Update/Delete داشبورد از میکسین‌های
`AjaxFormMixin` / `AjaxDeleteMixin` در `portal/views.py` استفاده می‌کنند و همچنان به‌صورت
صفحه‌ی کامل (fallback بدون جاوااسکریپت) هم قابل استفاده‌اند — مثلاً با ورود مستقیم به آدرس افزودن/ویرایش.

## ساختار پروژه

```
customs_guild/
├── manage.py
├── requirements.txt
├── customs_guild/            # تنظیمات پروژه (settings, urls, wsgi, asgi)
└── portal/                   # اپ اصلی سایت
    ├── models.py              # Specialization, Member(role), HSCode, NewsPost(jalali),
    │                          # CompletedWork(jalali), ContactMessage, HeroSlide
    ├── views.py                # ویوهای عمومی + AjaxFormMixin/AjaxDeleteMixin + CRUD داشبورد
    ├── forms.py                 # فرم‌های تماس/جست‌وجو + فرم‌های داشبورد (select2 / jalali widgets)
    ├── urls.py
    ├── admin.py                  # ثبت مدل‌ها + ویجت‌های تاریخ شمسی ادمین (django_jalali.admin)
    ├── context_processors.py      # اطلاعات پایه‌ی سایت + زمینه‌های فعالیت در دسترس همه‌ی قالب‌ها
    ├── management/commands/seed_data.py  # داده‌ی نمونه برای تست (شامل اسلاید و نقش اعضا)
    ├── migrations/0002_jalali_dates_role_heroslide.py
    ├── static/portal/{css,js}     # style.css + dashboard.css ، main.js + dashboard.js
    └── templates/portal/
        ├── {home,members,featured_members,member_detail,hs_code_search,news_*,completed_works,contact}.html
        └── dashboard/
            ├── base_dashboard.html        # شامل لینک‌های CDN: jQuery/Select2/SweetAlert2/persian-datepicker
            ├── generic_form_page.html     # قالب مشترکِ حالت بدون جاوااسکریپت
            ├── ajax/modal_form.html       # قالب فرم داخل مودال (پاسخ AJAX)
            ├── fragments/_*.html          # فقط ردیف‌های فیلد هر مدل (بدون تگ <form>)
            └── {member,news,work,hscode,specialization,slide}_list.html
```

## نکات مهم پیش از انتشار (Production)

1. مقدار `SECRET_KEY` در `customs_guild/settings.py` را با یک کلید تصادفی و محرمانه جایگزین کنید.
2. `DEBUG = False` کنید و `ALLOWED_HOSTS` را به دامنه‌ی واقعی محدود کنید.
3. برای پایگاه‌داده‌ی production، به‌جای SQLite از PostgreSQL استفاده کنید (`DATABASES` در settings.py).
4. `python manage.py collectstatic` را برای جمع‌آوری فایل‌های استاتیک اجرا کنید و آن‌ها را از طریق وب‌سرور (Nginx) یا سرویس CDN سرو کنید.
5. برای مدیای آپلودی (تصاویر اعضا/اخبار/نمونه‌کارها/اسلایدها)، از یک storage backend مناسب (مثل S3) استفاده کنید.
6. پروژه را پشت Gunicorn/uWSGI + Nginx اجرا کنید.
7. کتابخانه‌های CDN داشبورد (jQuery/Select2/SweetAlert2/persian-datepicker) را در صورت نیاز به کار آفلاین، محلی‌سازی کنید.

## توسعه‌های پیشنهادی بعدی

- اتصال به API رسمی گمرک ایران برای داده‌ی واقعی و به‌روز HS Code (در حال حاضر جست‌وجو روی داده‌ی محلیِ مدل `HSCode` انجام می‌شود).
- افزودن سامانه‌ی عضویت آنلاین با پرداخت حق عضویت.
- افزودن نقش‌های کاربری متفاوت در خودِ داشبورد (مثلاً مدیر محتوا در برابر مدیر کل)، جدا از فیلد «سمت» اعضای صنف.
- به‌روزرسانی سطرهای جدول در جای خود پس از افزودن/ویرایش/حذف با AJAX (در حال حاضر پس از موفقیت، صفحه رفرش می‌شود که ساده‌تر و پایدارتر است).

