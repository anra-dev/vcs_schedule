"""
ASGI config for vcs_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from utils import db

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vcs_site.settings')
db.database_ready("default", maximum_wait=15)
application = get_asgi_application()
