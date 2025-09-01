FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Créer un dossier de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copier et installer requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port (optionnel pour Railway)
EXPOSE 8000

# Commande de démarrage
ENV DJANGO_SETTINGS_MODULE=bluesky_tourism.settings

CMD sh -c "gunicorn bluesky_tourism.wsgi:application --bind 0.0.0.0:${PORT} --timeout 120 --log-level debug"
