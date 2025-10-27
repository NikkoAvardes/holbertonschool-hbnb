# 🏡 HBnB - Backend API avec Flask

## 📘 Description du projet

**HBnB** est une application backend conçue pour gérer des annonces de logements, inspirée du fonctionnement d’**Airbnb**.  
Ce projet a pour but d’implémenter une **API REST complète** permettant de gérer les entités principales du système : **utilisateurs, logements, avis et commodités**, en suivant une **architecture modulaire** et les **bonnes pratiques Flask**.

L’application met en œuvre les principes d’architecture logicielle tels que les **couches de présentation, logique métier et persistance**, tout en utilisant les **patterns Façade** et **Repository** pour garantir la maintenabilité et la scalabilité du code.

---

## 🎯 Objectifs du projet

- Construire une **API REST** modulaire et bien structurée avec Flask.  
- Implémenter la logique métier pour les entités principales :  
  `User`, `Place`, `Review`, `Amenity`.  
- Appliquer le **pattern Façade** pour isoler la logique métier.  
- Implémenter la **persistance en mémoire**, en prévision d’une base de données future.  
- Documenter automatiquement l’API via **Swagger (flask-restx)**.  
- Tester et valider tous les endpoints avec **Postman/cURL** et des **tests automatisés**.

---

## ⚙️ Architecture du projet

Le projet suit une **architecture en couches** :

```c
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```


### 🧩 Détails par couche

#### **1. Présentation (API)**
- `api/v1/` contient les endpoints REST (`users.py`, `places.py`, `reviews.py`, `amenities.py`).
- Gère la sérialisation, les statuts HTTP et la documentation Swagger.

#### **2. Logique métier (services)**
- `facade.py` implémente le **pattern Façade**.
- Centralise les appels entre l’API et la couche de persistance.
- Contient la logique métier : validation, gestion des relations, etc.

#### **3. Persistance (repository)**
- `repository.py` définit un **InMemoryRepository**.
- Fournit les opérations CRUD : `add`, `get`, `update`, `delete`, `get_all`.

#### **4. Modèles (models)**
- Chaque entité (`User`, `Place`, `Review`, `Amenity`) est représentée par une classe métier.

#### **5. Configuration et exécution**
- `config.py` : paramètres d’environnement (clé secrète, mode debug, etc.).
- `run.py` : point d’entrée de l’application Flask (`create_app()`).

---

## 🧱 Fonctionnalités principales

### 👤 Utilisateurs (`/api/v1/users/`)
- **POST** : créer un utilisateur  
- **GET** : récupérer tous les utilisateurs ou un utilisateur spécifique  
- **PUT** : mettre à jour un utilisateur

### 🏠 Logements (`/api/v1/places/`)
- **POST** : créer un logement avec validation des champs (prix, coordonnées GPS, etc.)  
- **GET** : lister ou consulter un logement spécifique  
- **PUT** : mettre à jour un logement et ses commodités associées  

### 🌟 Commodités (`/api/v1/amenities/`)
- **POST** : créer une commodité  
- **GET** : consulter toutes les commodités ou une seule  
- **PUT** : mettre à jour une commodité  
*(pas de suppression pour l’instant)*

### 📝 Avis (`/api/v1/reviews/`)
- **POST** : créer un avis lié à un logement et un utilisateur  
- **GET** : lister tous les avis ou en consulter un  
- **PUT** : modifier un avis  
- **DELETE** : supprimer un avis  

---

## 🧠 Patterns utilisés

### **Pattern Façade**
Simplifie les appels entre les routes API et la logique métier via une seule interface (`HBnBFacade`).

### **Pattern Repository**
Abstraction de la couche de persistance (stockage en mémoire pour le moment, extensible vers une base SQL plus tard).

---

## 🧰 Outils et technologies

- **Python 3.10+**
- **Flask** — Framework web principal
- **Flask-RESTX** — Documentation Swagger automatique
- **Postman / cURL** — Tests manuels
- **pytest** — Tests automatisés

---

## 💻 Installation et Setup

### 🪄 Prérequis
- Python 3.10 ou supérieur
- `pip` installé

### 🚀 Étapes d’installation

# 1. Cloner le dépôt
git clone https://github.com/<ton-username>/hbnb.git
cd hbnb

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate   # (ou venv\Scripts\activate sous Windows)

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l’application
python3 run.py

---

## ➡️ Accès à l’API

L’API est accessible sur :  
**http://0.0.0.0:5000/**  

### 🌐 Swagger UI
Documentation interactive disponible ici :  
**http://0.0.0.0:5000/api/v1/**

---

## 📚 API Documentation (Swagger)

La documentation interactive est générée automatiquement par **flask-restx**.  
Elle décrit tous les **endpoints**, les **formats de requêtes/réponses** et les **codes d’erreur** possibles.

---

## 🧪 Tests

Les tests ont été réalisés avec **Postman**, **Swagger** et des **tests unitaires automatiques**.

### ✅ Exemples de résultats

#### **Users**
| Action | Statut attendu | Statut obtenu |
|--------|----------------|---------------|
| POST User | 201 Created | ✅ |
| Invalid data | 400 Bad Request | ✅ |
| Email already used | 400 Bad Request | ✅ |
| GET all | 200 OK | ✅ |
| PUT update | 200 OK | ✅ |
| Not found | 404 Not Found | ✅ |

#### **Places / Amenities / Reviews**
Tous les endpoints CRUD ont été validés avec les statuts attendus :  
`200`, `201`, `400`, `404`, `409`, `204`.


### ✅ Exemples de tests :

![alt text](<img/Capture d'écran 2025-10-19 003748.png>)

![alt text](<img/Capture d'écran 2025-10-19 003705.png>)

![alt text](<img/Capture d'écran 2025-10-19 003647.png>)

![alt text](<img/Capture d'écran 2025-10-19 003420.png>)

---

## 👩‍💻 Développement

### 🧭 Lignes directrices
- Respect du **PEP8** (style Python)  
- Code **modulaire** et **réutilisable**  
- Validation des données dans la **couche logique métier**  
- Documentation claire pour chaque fonction  

### 🔁 Workflow de développement
1. Implémentation des modèles métier  
2. Création de la façade métier (`facade.py`)  
3. Définition des routes API (**Flask-RESTX**)  
4. Tests manuels et automatisés  
5. Documentation Swagger  

---


## 🚀 Améliorations futures

- 🔗 Intégration d’une **base de données persistante** (PostgreSQL ou SQLite)  
- 🧾 Authentification **JWT** (login/register)  
- ☁️ Déploiement sur **Render**, **AWS** ou **Docker**  
- 📈 Ajout de **tests automatisés de bout en bout**  
- 💬 Filtrage et recherche avancée (prix, localisation, commodités)  
- 🧩 Développement de la **version 2 de l’API (v2/)**  

---

## 👥 Auteurs

**Projet HBnB - Flask REST API**  
Développé dans le cadre du programme **Holberton School**  

🧠 Par : **Nina**  
🧠 Par : **Aurélie**  
🧠 Par : **Nicolai** 