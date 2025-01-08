# Utiliser l'image officielle de Python 3.12.7
FROM python:3.12.7-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requirements.txt contenant les dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application
COPY . .

# Exposer le port utilisé par Flask
EXPOSE 6666

# Définir la commande de démarrage du service Flask
CMD ["python", "app.py"]
