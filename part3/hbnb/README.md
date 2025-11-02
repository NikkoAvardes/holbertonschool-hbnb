# 🌐 HBNB – API RESTful avec gestion sécurisée et ORM

## 🎯 But du projet
Cette troisième partie du projet **HBnB** a pour but de construire une API complète et sécurisée qui connecte les modèles à une base de données SQL à l’aide de **Flask**, **JWT** et **SQLAlchemy**.  
L’objectif est de rendre l’application HBnB totalement exploitable via des endpoints REST : création d’utilisateurs, publication de logements, gestion des avis, et administration sécurisée.

---

## 🧩 Principaux objectifs
- 🔐 Mettre en place une **authentification JWT** (login / autorisations)
- 🧑‍💻 Implémenter des **rôles utilisateurs** (admin, propriétaire, invité)
- 🏗️ Créer une architecture modulaire et claire (API, services, persistance)
- 🗃️ Mapper les entités Python vers une **base SQL** avec SQLAlchemy
- ✅ Fournir un CRUD complet sur : `User`, `Place`, `Review`, `Amenity`
- 🧪 Rédiger des tests unitaires avec **pytest**
- 📖 Générer automatiquement une documentation Swagger grâce à Flask-RESTx

---

## 🧱 Architecture générale

```
├── 📁 SQL/
│ ├── 📄 data.sql → Données d'exemple
│ ├── 📄 schema.sql → Schéma de la base de données
│ └── 📄 test_crud.sql → Script de test des requêtes SQL

├── 📁 app/
│ ├── 📁 api/
| | └── 📄 init__.py → Initialisation du package api
| |     📁 v1/
│ │      ├── 📄 amenities.py → Endpoints REST pour les commodités
│ │      ├── 📄 auth.py → Endpoint de login JWT
│ │      ├── 📄 places.py → Endpoints REST pour les logements
│ │      ├── 📄 reviews.py → Endpoints REST pour les avis
│ │      ├── 📄 users.py → Endpoints REST pour les utilisateurs
│ │      └── 📄 init.py → Initialisation de la version 1 des routes
│ │
│ ├── 📁 models/
│ │ ├── 📄 amenity.py → Modèle Amenity
│ │ ├── 📄 base.py → Classe de base commune SQLAlchemy
│ │ ├── 📄 place.py → Modèle Place
│ │ ├── 📄 review.py → Modèle Review
│ │ ├── 📄 user.py → Modèle User (avec hash de mot de passe)
│ │ └── 📄 init.py → Permet l'import global des modèles
│ │
│ ├── 📁 persistence/
│ │ ├── 📄 repository.py → Accès aux données (CRUD)
│ │ └── 📄 init.py → Initialisation du package de persistance
│ │
│ ├── 📁 services/
│ │ ├── 📄 facade.py → Contient la couche de service, abstraction entre endspoints (API) et persistance des données
│ │ └── 📄 init.py → Permet d’organiser les services métier
│ │
│ └── 📄 extensions.py → Initialisation des extensions Flask (JWT, Bcrypt, DB)
| └── 📄 init.py → Création de l'application Flask

├── 📁 tests/
│ └── 📄 test_user_model_pawd.py → Test du modèle utilisateur

├── 📁 instance/
│ └── 📄 dev.db → Contient les tables SQLAlchemy générées automatiquement

├── 📁 images/ → Contient les ressources visuelles du projet (schémas, diagrammes, etc.)
│

├── 📄 config.py → Configuration Flask (dev/prod)
├── 📄 requirements.txt → Dépendances Python
├── 📄 run.py → Point d’entrée pour lancer l’API
```



---

## 🧠 Fonctionnalités essentielles

### 👤 Gestion des utilisateurs
- Création et mise à jour sécurisée via JSON
- Mots de passe hachés avec **Flask-Bcrypt**
- Rôle `is_admin` pour les comptes privilégiés
- Accès restreint aux données personnelles

### 🏡 Gestion des logements 
- Reliés à un utilisateur propriétaire (`owner_id`)
- Contiennent les coordonnées GPS (latitude / longitude)
- Liés à plusieurs commodités (`amenities`)
- Validation stricte des champs envoyés

### 💬 Avis 
- Chaque avis appartient à un utilisateur et un logement
- Champs : note (rating), contenu du texte, date
- Seul l’auteur ou un admin peut modifier/supprimer

### 🪑 Commodités
- CRUD complet sauf suppression
- Nom unique, limité à 50 caractères
- Association via une table de liaison avec les `Places`

### 🔑 Authentification JWT
- Login via `/api/v1/auth/login`
- Token transmis dans le header : `Authorization: Bearer <token>`
- Décodage automatique via le décorateur `@jwt_required()`
- Le mot de passe n’est **jamais retourné** dans les réponses JSON

---

## ⚙️ Installation & Démarrage

### 🔧 Prérequis
- Python 3.12 ou plus récent  
- pip et virtualenv

### 🚀 Étapes d’installation
```bash
git clone https://github.com/Aluranae/holbertonschool-hbnb.git
cd part3/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

---

### ▶️ Lancement du serveur

```bash
python run.py
```

Le serveur démarre sur `http://127.0.0.1:5000/`

##  Exemple d’utilisation:

###  Authentification (login)
```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login   -H "Content-Type: application/json"   -d '{"email": "user@example.com", "password": "userpwd"}'
```

###  Accès protégé avec JWT

```bash
curl -X GET http://127.0.0.1:5000/api/v1/users/me   -H "Authorization: Bearer <your_token>"
```

###  Création d'une place
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places   -H "Authorization: Bearer <your_token>"   -H "Content-Type: application/json"   -d '{"name": "My Flat", "description": "Nice place"}'
```

###  Ajout d'un avis
```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews   -H "Authorization: Bearer <your_token>"   -H "Content-Type: application/json"   -d '{"place_id": "<place_id>", "text": "Great stay!", "rating": 5}'
```

###  Création d'une commodité
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities   -H "Authorization: Bearer <admin_token>"   -H "Content-Type: application/json"   -d '{"name": "WiFi"}'
```

###  Suppression d'une review
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review_id>   -H "Authorization: Bearer <your_token>"
```


---


##  tests :

![alt text](<../img/Capture d’écran (79).png>)

![alt text](<../img/Capture d’écran (80).png>)

![alt text](<../img/Capture d’écran (81).png>)

## diagram :

![alt text](<../img/Capture d'écran 2025-11-02 152745.png>)

---

## Technologies utilisées

- **Python 3.12**
- **Flask**
- **Flask-RESTx**
- **Flask-JWT-Extended**
- **Flask-Bcrypt**
- **SQLAlchemy** (mapping)
- **pytest** (tests éventuels)



## 👥 Auteurs

- Nina
- Aurélie
- Nicolai
