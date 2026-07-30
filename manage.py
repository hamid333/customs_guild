#!/usr/bin/env python
"""ابزار خط‌فرمان مدیریت پروژه‌ی جنگو (Django's command-line utility)."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django قابل ایمپورت نیست. مطمئن شوید نصب شده و در PYTHONPATH قرار دارد. "
            "آیا محیط مجازی (virtualenv) را فعال کرده و pip install -r requirements.txt را اجرا کرده‌اید؟"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
