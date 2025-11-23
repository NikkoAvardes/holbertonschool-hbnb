# 🏠 HBnB – Plateforme de location collaborative

Bienvenue dans la dernière étape du projet HBnB, conçu pour le cursus Holberton School.  
Ce projet Full-Stack, inspiré d’AirBnB, combine une API robuste, une base de données relationnelle et une interface web moderne pour offrir une expérience utilisateur complète : publier, explorer et commenter des logements en toute sécurité.

---

## 🧭 Sommaire
- [Présentation](#présentation)
- [Architecture & Phases](#architecture--phases)
- [Fonctionnalités](#fonctionnalités)
- [Installation & Lancement](#installation--lancement)
- [Auteurs](#auteurs)

---

## Présentation

HBnB est une application collaborative de location de logements, pensée pour apprendre les principes de l’architecture logicielle, la sécurité web et l’intégration front-end.  
Le projet se construit en quatre grandes étapes, chacune approfondissant un aspect du développement web moderne.

---

## Architecture & Phases

### 1️⃣ Modélisation & UML
- Conception des entités (`User`, `Place`, `Review`, `Amenity`) et de leurs relations
- Diagrammes de classes, séquences et organisation des packages
- Documentation technique pour guider l’implémentation

### 2️⃣ Logique métier & API REST
- Développement des modèles métiers et endpoints CRUD avec Flask/Flask-RESTx
- Application du pattern Façade pour la logique métier
- Tests manuels via Postman/cURL

### 3️⃣ Authentification & Base de données
- Intégration de SQLAlchemy ORM (SQLite/MySQL)
- Gestion des relations complexes (1-N, N-N)
- Authentification JWT, rôles utilisateurs, sécurisation des endpoints
- Validation et intégrité des données

### 4️⃣ Interface Web interactive

La quatrième phase introduit le front-end : une interface web dynamique qui dialogue avec l’API.  
Objectif : permettre aux utilisateurs de naviguer, filtrer, se connecter et publier des avis en temps réel.

---

## Fonctionnalités

- **Accueil dynamique** : liste des logements, filtrage par prix
- **Connexion sécurisée** : gestion du JWT dans les cookies
- **Détail d’un logement** : description, hôte, prix, commodités, avis
- **Ajout d’avis** : formulaire accessible uniquement aux utilisateurs connectés
- **Navigation fluide** : transitions sans rechargement complet
- **Design responsive** : adapté à tous les écrans
- **Séparation claire** : API backend et client web indépendants

---

## Installation & Lancement

### Prérequis
- Python ≥ 3.12
- pip et virtualenv

### Installation
```bash
cd part4/hbnb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Démarrage du serveur
```bash
python3 run.py
```
Accède à l’application sur : [http://127.0.0.1:5000](http://127.0.0.1:5000)  
Pour arrêter le serveur : `CTRL + C`

---

## Technologies

- Python 3.12, Flask, Flask-RESTx, Flask-JWT-Extended, Flask-Bcrypt, SQLAlchemy, pytest
- HTML5, CSS3, JavaScript ES6

---

## 👥 Équipe

- Nina
- Aurélie
- Nicolai

## Technologies utilisées

- **Python 3.12**
- **Flask**
- **Flask-RESTx**
- **Flask-JWT-Extended**
- **Flask-Bcrypt**
- **SQLAlchemy** (mapping)

