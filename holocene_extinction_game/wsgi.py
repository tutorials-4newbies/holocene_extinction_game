"""
WSGI config for holocene_extinction_game project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holocene_extinction_game.settings')

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
