"""
WSGI config for advanced_api_project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')

application = get_wsgi_application()