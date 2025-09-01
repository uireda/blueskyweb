FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DEBUG=True

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Collection des fichiers statiques
RUN python manage.py collectstatic --noinput

# Port d'exposition
EXPOSE 8000

# Commande de démarrage
CMD ["sh", "-c", "echo 'Starting Django...' && python manage.py makemigrations && python manage.py migrate && python manage.py check && gunicorn --bind 0.0.0.0:$PORT --log-level debug bluesky_tourism.wsgi:application"]