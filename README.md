# 🏠 AirBnB Clone – HBnB Project

Un projet complet de plateforme de location inspiré d’**AirBnB**, développé dans le cadre du cursus **Holberton School**.  
Il s’agit de l’un des projets les plus importants du programme, réalisé en équipe, visant à construire une application **Full-Stack** alliant architecture, back-end, et interface web.

Ce clone d’AirBnB permet aux utilisateurs de publier, rechercher et réserver des logements, tout en offrant un système d’authentification sécurisé et une base de données relationnelle robuste.  
Le projet est conçu selon une **architecture modulaire** et suit une progression en quatre grandes phases, de la modélisation UML à la création du client web.

---

## 🧭 Table des matières
- [📘 Introduction](#-introduction)
- [🏗️ Architecture du projet](#️-architecture-du-projet)
- [🧩 Fonctionnalités principales](#-fonctionnalités-principales)
- [⚙️ Installation & Démarrage](#️-installation--démarrage)
- [📡 Exemples d’utilisation (curl)](#-exemples-dutilisation-curl)
- [🧪 Tests automatisés](#-tests-automatisés)
- [🧰 Stack technique](#-stack-technique)
- [👥 Auteurs](#-auteurs)

---

## 📘 Introduction
Le projet **HBnB** a pour objectif de reproduire les fonctionnalités essentielles d’AirBnB à travers une approche pédagogique complète.  
Il est divisé en plusieurs étapes qui permettent d’aborder la conception d’API, la gestion des bases de données, la sécurité des utilisateurs et l’intégration d’un front-end dynamique.

Chaque partie du projet approfondit un aspect différent du développement web complet, en suivant les bonnes pratiques d’architecture et de documentation.

---

## 🏗️ Architecture du projet

### 1️⃣ HBnB - UML
Première phase : conception de l’architecture de l’application via **UML**.  
Objectif : modéliser les entités principales (`User`, `Place`, `Review`, `Amenity`) et leurs relations pour préparer le développement.  
Les diagrammes produits :
- Diagrammes de classes et de séquences  
- Organisation des packages et flux de données  
- Documentation technique servant de base à toute l’implémentation  

---

### 2️⃣ HBnB - Business Logic & API
Deuxième étape : développement du cœur applicatif et des routes **RESTful** à l’aide de **Flask** et **Flask-RESTx**.  
- Définition des modèles métiers : `User`, `Place`, `Review`, `Amenity`  
- Application du **pattern Façade** pour isoler la logique métier  
- Création des endpoints CRUD (Create, Read, Update, Delete)  
- Tests manuels via Postman et cURL  

> 🔒 À ce stade, aucune authentification ni base de données persistante — l’accent est mis sur la structure et la cohérence du code.

---

### 3️⃣ HBnB - Auth & Database
Troisième étape : ajout de la **base de données** et du **système d’authentification JWT**.  
- Migration vers **SQLAlchemy ORM** avec une base **SQLite/MySQL**  
- Gestion complète des relations (1-N et N-N)  
- Authentification et rôles utilisateurs (admin / user)  
- Sécurisation des endpoints avec tokens JWT  
- Validation et intégrité des données  

Cette étape rend le back-end prêt pour un déploiement réel.

---

### 4️⃣ HBnB - Simple Web Client
...

---

## 🧩 Fonctionnalités principales

### 🏡 Gestion des logements (Places)
- Reliés à un utilisateur propriétaire (`owner_id`)  
- Coordonnées GPS (latitude / longitude)  
- Liés à plusieurs commodités (`amenities`)  
- Validation stricte des champs  

### 💬 Avis (Reviews)
- Chaque avis appartient à un utilisateur et un logement  
- Champs : note (rating), texte, date  
- Seul l’auteur ou un admin peut modifier/supprimer  

### 🪑 Commodités (Amenities)
- CRUD complet sauf suppression  
- Nom unique (max 50 caractères)  
- Association via une table de liaison avec les `Places`  

### 🔑 Authentification JWT
- Login via `/api/v1/auth/login`  
- Token dans le header : `Authorization: Bearer <token>`  
- Décodage automatique avec `@jwt_required()`  
- Le mot de passe n’est **jamais retourné**  

---

## ⚙️ Installation & Démarrage

### 🔧 Prérequis
- Python ≥ 3.12  
- pip et virtualenv installés  

### 🚀 Installation
```bash
git clone https://github.com/<ton_nom_d_utilisateur>/<ton_repo>.git
cd <ton_repo>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


## 👥 Auteurs

- Nina
- Aurélie
- Nicolai