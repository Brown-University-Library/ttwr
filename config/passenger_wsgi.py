"""
WSGI config for etd project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from sys import path
from django.core.wsgi import get_wsgi_application

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path.append(SITE_ROOT)

activate_this = os.path.join(os.path.dirname(SITE_ROOT),'env/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

application = get_wsgi_application()
