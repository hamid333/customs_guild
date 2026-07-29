"""
WSGI config for customs_guild project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customs_guild.settings")

application = get_wsgi_application()
