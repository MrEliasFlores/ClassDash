"""
WSGI config for ClassDash project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

path = '/home/pi/ClassDash'

if path not in sys.path:
        sys.path.append(path)
        
sys.path.append('home/pi/ClassDash/')
sys.path.append('home/pi/ClassDash/ClassDash/')
        
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClassDash.settings')

application = get_wsgi_application()
