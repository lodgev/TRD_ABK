# Utiliser l'image officielle de Python
FROM python:3.12.7-slim

# Installer les bibliothèques nécessaires
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY . .

# Exposer le port de Flask
EXPOSE 6666

# Lancer l'application Flask
CMD ["python", "app.py"]
