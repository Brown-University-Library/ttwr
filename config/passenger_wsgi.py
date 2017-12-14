import os
from sys import path
import dotenv

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.append(SITE_ROOT)

dotenv.read_dotenv(join(SITE_ROOT, '.env'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
