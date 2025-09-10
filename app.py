import os
import sys

# Ajouter le dossier du projet au Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluesky_tourism.settings')

# Import de l'application Django
from django.core.wsgi import get_wsgi_application

# Initialiser Django
application = get_wsgi_application()

# Variables requises par Vercel
app = application
handler = application