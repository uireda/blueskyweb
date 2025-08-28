import os
from django.core.wsgi import get_wsgi_application

# Important : définir la variable d'environnement AVANT d'importer quoi que ce soit de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluesky_tourism.settings')

# Pour Vercel, on doit s'assurer que Django est configuré
application = get_wsgi_application()

# Vercel cherche ces variables
app = application
handler = application