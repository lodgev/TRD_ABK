# Architecture Micro Services modèle - Python (FastAPI) + Docker (PoC)

🚨🚨🚨 Preuve de concept (work in progress) 🚨🚨🚨

TODO:

- les fichiers suivants n'ont pas d'effet. Ils sont donnés à titre d'exemple. Seuls les fichiers __./tasks-db/init.sql__ et __./auth-db/init.sql__ sont réellement utilisés pour initier chaque base de données Postgresql (auth-db et tasks-db):
  - ./tasks-db/1-schema.sql
  - ./tasks-db/2-data.sql
  - ./auth-db/1-schema.sql
  - ./auth-db/2-data.sql
- les services Python ne sont pas connectés à leur base de données respective
- le service auth n'est pas implémenté (signin, signup, signout, verify token...)
- le service gateway n'est pas implémenté
- l'API REST du service tasks est fictive (données statiques / pas de connexion à la BDD)
- les services Python et BDD sont accessibles depuis l'extérieur du réseau : ils ne devraient pas l'être. Seul le service gateway devrait être accessible depuis l'extérieur
- le dossier flask-service contient un service modèle réalisé avec Flask qui peut être utilisé à la place de FastAPI

## Instructions pour l'installation (avant le lancement des services Docker)

- créer les fichiers de variables d'environnement en se basant sur les fichiers modèles nommés .env.example :

- ./gateway-service/.env
- ./auth-service/.env
- ./auth-db/.env
- ./tasks-service/.env
- ./tasks-db/.env
- ./rabbitmq/.env

## Adminer

- Pour accéder à l'exploration des Bases de données Postgresql dans __Adminer__, sélectionner le type __"Postgresql"__.
- Le nom de l'hôte de la BDD correspond au nom du service (ex: auth-db ou tasks-db).

## Lancement des services Docker

### Sans reconstruction des images Docker

```sh
docker compose up
```

### Sans reconstruction des images Docker + activation du mode watch (permet de reconstruire en live les containers en cas de modification du code source)

```sh
docker compose up --watch
```

### Avec reconstruction des images Docker au lancement (si modification du code source associé)

```sh
docker compose up --build
```

### Avec reconstruction des images Docker au lancement (si modification du code source associé) + activation du mode watch (permet de reconstruire en live les containers en cas de modification du code source)

```sh
docker compose up --build --watch
```

### Suppression des containers

```sh
docker compose down
```

--

!["Logotype Shrp"](https://sherpa.one/images/sherpa-logotype.png)

__Alexandre Leroux__  
_Enseignant / Formateur_  
_Développeur logiciel web & mobile_

Nancy (Grand Est, France)

<https://shrp.dev>
