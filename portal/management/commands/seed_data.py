"""
دستور مدیریتی برای پرکردن پایگاه‌داده با داده‌ی نمونه (Demo Data).
اجرا:
    python manage.py seed_data
"""
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from portal.models import Specialization, Member, HSCode, NewsPost, CompletedWork


class Command(BaseCommand):
    help = "پرکردن پایگاه‌داده با داده‌ی نمونه برای تست سریع سایت"

    def handle(self, *args, **options):
        self.stdout.write("در حال ایجاد داده‌ی نمونه...")

        # ---------------- زمینه‌های فعالیت ----------------
        spec_titles = [
            "ترخیص کالای صنعتی", "واردات خودرو", "صادرات کالا",
            "امور بنادر و فرودگاه‌ها", "ترخیص کالای دارویی", "لجستیک و حمل‌ونقل بین‌المللی",
        ]
        specs = []
        for title in spec_titles:
            spec, _ = Specialization.objects.get_or_create(
                title=title, defaults={"slug": slugify(title, allow_unicode=True)}
            )
            specs.append(spec)

        # ---------------- اعضا ----------------
        members_data = [
            {"full_name": "شرکت ترخیص کالای پارسیان", "membership_no": "TC-1001", "city": "تهران", "established_year": 1388, "is_featured": True},
            {"full_name": "مؤسسه‌ی حق‌العمل‌کاری آریا گمرک", "membership_no": "TC-1002", "city": "بندرعباس", "established_year": 1392, "is_featured": True},
            {"full_name": "شرکت بازرگانی و ترخیص کاسپین", "membership_no": "TC-1003", "city": "انزلی", "established_year": 1395, "is_featured": True},
            {"full_name": "گروه ترخیص و لجستیک البرز", "membership_no": "TC-1004", "city": "تهران", "established_year": 1390, "is_featured": True},
        ]
        members = []
        for i, data in enumerate(members_data):
            m, _ = Member.objects.get_or_create(membership_no=data["membership_no"], defaults={
                "full_name": data["full_name"],
                "city": data["city"],
                "established_year": data["established_year"],
                "is_featured": data["is_featured"],
                "bio": "این عضو با سال‌ها تجربه در حوزه‌ی ترخیص و امور گمرکی، خدمات تخصصی به بازرگانان ارائه می‌دهد.",
                "phone": "021-8000000" + str(i),
                "status": Member.STATUS_ACTIVE,
            })
            m.specializations.add(specs[i % len(specs)], specs[(i + 1) % len(specs)])
            members.append(m)

        # ---------------- ردیف‌های تعرفه (HS Code) ----------------
        hs_data = [
            ("8703.23", "خودروی سواری با حجم موتور ۱۵۰۰ تا ۳۰۰۰ سی‌سی", "Motor cars, 1500-3000cc", "خودرو", "32٪"),
            ("0901.21", "قهوه بوداده، بدون کافئین‌زدایی", "Roasted coffee, not decaffeinated", "مواد غذایی", "10٪"),
            ("8517.12", "تلفن همراه", "Mobile phones", "الکترونیک", "4٪"),
            ("6109.10", "تی‌شرت و زیرپیراهن‌های کشباف از پنبه", "T-shirts, cotton, knitted", "نساجی", "26٪"),
            ("3004.90", "داروهای مخلوط یا ساخته‌نشده برای خرده‌فروشی", "Medicaments, mixed/unmixed", "دارویی", "4٪"),
        ]
        for code, fa, en, cat, duty in hs_data:
            HSCode.objects.get_or_create(code=code, defaults={
                "title_fa": fa, "title_en": en, "category": cat, "duty_rate": duty,
            })

        # ---------------- اخبار ----------------
        news_data = [
            ("بخشنامه‌ی جدید گمرک درباره‌ی ترخیص کالاهای اساسی", "خلاصه‌ای از آخرین بخشنامه‌ی گمرک ایران درباره‌ی رویه‌ی ترخیص کالاهای اساسی منتشر شد."),
            ("برگزاری مجمع عمومی سالانه‌ی انجمن", "مجمع عمومی سالانه‌ی انجمن با حضور اعضای فعال صنف برگزار می‌شود."),
            ("راه‌اندازی سامانه‌ی جدید جست‌وجوی HS Code", "سامانه‌ی جست‌وجوی آنلاین ردیف‌های تعرفه برای تسهیل کار اعضا و بازرگانان راه‌اندازی شد."),
        ]
        for i, (title, summary) in enumerate(news_data):
            NewsPost.objects.get_or_create(slug=slugify(title, allow_unicode=True), defaults={
                "title": title, "summary": summary,
                "body": summary + "\n\nمتن کامل این خبر به‌زودی تکمیل خواهد شد.",
                "published_at": date.today() - timedelta(days=i * 3),
            })

        # ---------------- نمونه‌کارها ----------------
        works_data = [
            ("ترخیص محموله‌ی ماشین‌آلات صنعتی از بندر شهید رجایی", "واردات صنعتی"),
            ("صادرات محموله‌ی خشکبار به کشورهای همسایه", "صادرات"),
            ("ترخیص تجهیزات پزشکی وارداتی", "دارویی/پزشکی"),
            ("ترخیص خودروهای وارداتی نمایشگاهی", "خودرو"),
        ]
        for i, (title, cat) in enumerate(works_data):
            CompletedWork.objects.get_or_create(title=title, defaults={
                "category": cat,
                "description": "شرح مختصر این پرونده و مراحل انجام آن توسط تیم تخصصی عضو مربوطه.",
                "member": members[i % len(members)],
                "completed_date": date.today() - timedelta(days=i * 10),
            })

        self.stdout.write(self.style.SUCCESS("داده‌ی نمونه با موفقیت ایجاد شد."))
