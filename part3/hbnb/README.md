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
part3/
└── 📁 hbnb/
    ├── 📄 README.md
    ├── 📄 config.py
    ├── 📄 requirements.txt
    ├── 📄 run.py
    ├── 📁 app/
    │   ├── 📄 __init__.py
    │   ├── 📁 api/
    │   │   ├── 📄 __init__.py
    │   │   └── 📁 v1/
    │   │       ├── 📄 __init__.py
    │   │       ├── 📄 amenities.py → Endpoints REST pour les commodités
    │   │       ├── 📄 auth.py → Endpoint de login JWT
    │   │       ├── 📄 places.py → Endpoints REST pour les logements
    │   │       ├── 📄 protected.py → Endpoints protégés par JWT
    │   │       ├── 📄 reviews.py → Endpoints REST pour les avis
    │   │       └── 📄 users.py → Endpoints REST pour les utilisateurs
    │   ├── 📁 models/
    │   │   ├── 📄 __init__.py → Permet l'import global des modèles
    │   │   ├── 📄 amenity.py → Modèle Amenity
    │   │   ├── 📄 base_model.py → Classe de base commune SQLAlchemy
    │   │   ├── 📄 place.py → Modèle Place
    │   │   ├── 📄 review.py → Modèle Review
    │   │   └── 📄 user.py → Modèle User (avec hash de mot de passe)
    │   ├── 📁 persistence/
    │   │   ├── 📄 __init__.py → Initialisation du package de persistance
    │   │   └── 📄 repository.py → Accès aux données (CRUD)
    │   └── 📁 services/
    │       ├── 📄 __init__.py → Permet d'organiser les services métier
    │       ├── 📄 facade.py → Couche de service, abstraction entre endpoints et persistance
    │       └── 📁 repositories/
    │           ├── 📄 __init__.py → Initialisation des repositories spécialisés
    │           └── 📄 user_repository.py → Repository spécialisé pour les utilisateurs
    ├── 📁 sql_scripts/
    │   ├── 📄 create_tables.sql → Script de création du schéma de la base
    │   └── 📄 insert_data.sql → Script d'insertion des données initiales
    ├── 📁 tests/
    │   ├── 📄 __init__.py → Initialisation du package de tests
    │   ├── 📄 run_all_tests.py → Lance tous les tests automatiquement
    │   ├── 📄 test_amenity_endpoints.py → Tests des endpoints amenities
    │   ├── 📄 test_place_endpoints.py → Tests des endpoints places
    │   ├── 📄 test_review_endpoints.py → Tests des endpoints reviews
    │   └── 📄 test_user_endpoints.py → Tests des endpoints users
	├── 📁 img/ → Ressources visuelles du projet (captures, schémas, etc.)
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

### Création d’un utilisateur administrateur
Cette capture montre le formulaire pour créer un nouvel utilisateur avec le rôle admin.
![alt text](<../hbnb/img/Create user_admin.png>)

---

### Connexion en tant qu’administrateur
Ici, l’admin se connecte pour accéder aux fonctionnalités avancées.
![alt text](<../hbnb/img/Login as Admin.png>)

---

### Création d’un utilisateur par l’admin (avec token)
L’admin peut créer d’autres utilisateurs grâce à son token d’authentification.
![alt text](<../hbnb/img/Admin create User (token).png>)

---

### Mise à jour d’un utilisateur par l’admin (avec token)
L’admin modifie les informations d’un utilisateur existant.
![alt text](<../hbnb/img/Admin update User (token).png>)

---

### Création d’un logement par l’admin (avec token)
L’admin ajoute un nouveau logement à la plateforme.
![alt text](<../hbnb/img/Admin create Place (token).png>)

---

## Diagramme de la base de données
Ce schéma illustre les relations entre les différentes tables du projet.
![alt text](<../hbnb/img/Database Diagrams.png>)


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
