"""
WSGI config for vcs_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from utils import db

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vcs_site.settings')
db.database_ready("default", maximum_wait=15)
application = get_wsgi_application()
