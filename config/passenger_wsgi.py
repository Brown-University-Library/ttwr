import os
from sys import path
import dotenv

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SITE_ROOT not in path:
    path.append(SITE_ROOT)

PROJECT_ROOT = dirname(SITE_ROOT)
dotenv.read_dotenv(os.path.join(PROJECT_ROOT, '.env'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
