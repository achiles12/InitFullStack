import os
from django.core.wsgi import get_wsgi_application

# Tell Django which settings module to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create the WSGI application object
application = get_wsgi_application()
