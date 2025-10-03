# 📘 HBnB – Technical Documentation

## 📖 Introduction
Ce document constitue la documentation technique du projet **HBnB**.  
Il regroupe les diagrammes et explications nécessaires pour comprendre l'architecture du système, les règles métiers, et les interactions entre les différentes couches de l'application.

**Objectifs du document :**
- Servir de référence technique pour l'équipe de développement.
- Décrire clairement l'architecture en couches (Presentation, Business, Persistence).
- Présenter les modèles principaux et leurs relations.
- Montrer les flux d'interaction API via des diagrammes de séquence.
- Expliquer les choix de conception (ex. utilisation du pattern *Façade*).

---

## 🏗️ High-Level Architecture

### Diagramme de Packages

![alt text](<Package Diagram.png>)

### Explications
L'architecture de HBnB est organisée en **3 couches principales** :

1. **Presentation Layer**
   - Contient les `Controllers` (UserController, PlaceController, ReviewController, AmenityController).
   - Sert d'interface entre l'utilisateur (ou un client API) et l'application.
   - Exemple : clic sur "Réserver un logement" → le controller reçoit la demande et l'envoie à la logique métier.

2. **Business Logic Layer**
   - Contient les modèles principaux : `User`, `Place`, `Review`, `Amenity`.
   - Applique les règles métiers (validation, cohérence des données, autorisations).
   - Exemple : empêcher un utilisateur de laisser un avis sans avoir réservé.

3. **Persistence Layer**
   - Contient les `Repositories` (UserRepository, PlaceRepository, ReviewRepository, AmenityRepository).
   - Gère la lecture/écriture des données dans la base.
   - Exemple : enregistrer un nouvel utilisateur validé par la logique métier.

**Façade Pattern :**
- La classe `HBNB_Facade` centralise les appels aux modèles pour simplifier l'usage.
- Elle agit comme une "réception" : l'utilisateur ne contacte pas directement les modèles mais passe par la façade.

---

## 🧩 Business Logic Layer – Class Diagram

### Diagramme de Classes

![alt text](<Class Diagram for Business Logic Layer.png>)

### Explications

#### **Base_model**
- Classe mère commune à tous les modèles.
- Attributs : `id (UUID)`, `created_at`, `updated_at`.
- But : factoriser les infos de base (identifiant et timestamps).

#### **User**
- Représente un utilisateur.
- Attributs : `first_name`, `last_name`, `email`, `password (privé)`, `is_admin`.
- Méthodes : `registerUser()`, `updateUser()`, `deleteUser()`.

#### **Place**
- Représente un logement/annonce.
- Attributs : `title`, `description`, `price`, `latitude`, `longitude`.
- Méthodes : `createPlace()`, `updatePlace()`, `deletePlace()`, `listPlace()`.

#### **Review**
- Représente un avis utilisateur.
- Attributs : `rating`, `comment`.
- Méthodes : `createReview()`, `updateReview()`, `deleteReview()`, `listReview()`.

#### **Amenity**
- Représente un équipement ou service (ex. wifi, piscine).
- Attributs : `name`, `description`.
- Méthodes : `createAmenity()`, `updateAmenity()`, `deleteAmenity()`, `listAmenity()`.

#### **HBNB_Facade**
- Interface unique pour interagir avec le système.
- Méthodes : `get()`, `delete()`, `add()`, `save()`, `list()`, `reload()`, `register()`, `count()`.
- Simplifie l'utilisation en centralisant les opérations CRUD.

---

## 🔄 API Interaction Flow – Sequence Diagrams

### 1️⃣ Création d'un **Place**

![alt text](<Place Sequence Diagram.png>)

### Explications

- Authentification : vérifie d'abord si l'utilisateur est connecté.

- Validation des règles métiers : contrôle que toutes les données obligatoires sont présentes et cohérentes.

- Sauvegarde : enregistre dans la base de données si la validation réussit.

### Réponses possibles :
- 401 Unauthorized → utilisateur non connecté.

- 400 Bad Request → données invalides.

- 201 Created → Place créé avec succès.

- 500 Internal Server Error → erreur lors de l'enregistrement en base.

### Scénario : Alice veut créer un nouveau logement sur HBnB.

- Déroulement technique, étape par étape 
Alice clique sur "Créer un logement" sur le site ou l'application.
Le client (navigateur ou application) envoie une requête POST /places contenant les informations du logement.
L'API reçoit la requête et vérifie si Alice est connectée :
Si Alice n'est pas connectée, l'API renvoie 401 Unauthorized et le client affiche "Connexion requise".
Si Alice est authentifiée, l'API transmet la requête à la Business Logic (BL) pour traitement :

### La BL valide les règles métier, par exemple :

Tous les champs obligatoires sont remplis (titre, description, prix, localisation).
Les valeurs sont cohérentes (prix positif, coordonnées valides…).
Si la validation échoue, la BL renvoie une erreur à l'API → 400 Bad Request, et le client affiche un message d'erreur.
Si la validation réussit, la BL tente de sauvegarder le logement en base de données via le Repository :
Si la base rencontre une erreur → API renvoie 500 Internal Server Error, le client affiche un message d'erreur.
Si la sauvegarde est réussie → API renvoie 201 Created, et le client affiche "Logement créé avec succès" avec l'ID du logement.

### Exemple :

Alice oublie de mettre un titre → elle reçoit 400 Bad Request, message : "Le titre est obligatoire".
Alice complète correctement tous les champs → le logement est créé, 201 Created, confirmation affichée.

---
## Création d'un Review

![alt text](<Review Sequence Diagrams.png>)
-----
### explications

- Validation des données : vérifie que le texte et la note sont valides → 400 Bad Request si non.

- Règles métiers : empêche l'utilisation de mots interdits → 403 Forbidden.

### Sauvegarde en base :

- 500 Internal Server Error → si la base échoue ou viole une contrainte.

- 201 Created → si l'avis est créé avec succès et retourne un Review ID.

### Scénario : Bob souhaite laisser un avis sur un logement qu'il a réservé.

### Déroulement technique, étape par étape :

Bob remplit le formulaire d'avis avec le texte et la note (rating).
Le client envoie une requête POST /reviews contenant review_text, rating et user_id.
L'API reçoit la requête et vérifie si Bob est connecté.
Si Bob n'est pas connecté, l'API renvoie 401 Unauthorized et le client affiche "Connexion requise".

Si Bob est authentifié, l'API transmet la requête à la Business Logic Layer pour validation :

Validation des données : texte non vide et note comprise entre 1 et 5.
Si les données sont invalides → 400 Bad Request.
Application des règles métier : pas de mots interdits, l'utilisateur doit avoir réservé le logement.
Si une règle est violée → 403 Forbidden.
Si tout est correct, la Business Logic Layer appelle le ReviewRepository pour enregistrer l'avis en base.
Si la base échoue → 500 Internal Server Error.
Si l'enregistrement réussit → 201 Created, et l'API renvoie l'ID du Review.

### Exemple concret :

Bob écrit un avis vide → il reçoit 400 Bad Request avec le message "Le texte de l'avis est obligatoire".
Bob écrit un avis avec des mots interdits → il reçoit 403 Forbidden avec le message "Mots interdits détectés".
Bob écrit un avis valide → il reçoit 201 Created, l'avis est enregistré et un Review ID lui est renvoyé, confirmation affichée sur le site.

### Fectching Place diagramme

![alt text](<Fetching_Place Sequence Diagrams.png>)

### Explications

- Validation des critères : l’API vérifie que les paramètres envoyés (ville, prix, etc.) sont valides.
→ 400 Bad Request si les critères sont invalides.

- Recherche en base : si les critères sont valides, l’application interroge la base pour trouver les logements correspondants.

### Résultats possibles :

- 200 OK + liste de logements → si des résultats sont trouvés.

- 200 OK + liste vide → si aucun logement ne correspond.

**Scénario : Alice souhaite rechercher un logement à Paris dans son budget.**
### Déroulement technique, étape par étape :

Alice remplit le formulaire de recherche (ville = Paris, prix < 100€/nuit, etc.).

Le client envoie une requête GET /places?city=Paris&price<100.

L’API reçoit la requête et appelle le PlaceModel pour valider les critères :
Ville doit être une chaîne valide.
Le prix doit être un nombre positif.
Si un critère est incorrect → 400 Bad Request avec le message "Invalid search parameters".
Si les critères sont valides, le PlaceModel interroge la base de données avec les filtres fournis.

**Deux cas possibles :**

Résultats trouvés → la base renvoie une liste de logements, l’API retourne 200 OK avec la liste (objets JSON).
Aucun résultat → la base renvoie une liste vide, l’API retourne 200 OK avec "Empty list".

### Exemple concret :

Alice envoie une recherche avec un prix négatif → l’API renvoie 400 Bad Request avec le message "Invalid search parameters".
Alice cherche à Paris avec un prix max 100€ → l’API renvoie 200 OK avec une liste de 3 logements.
Alice cherche à New York avec un prix max 10€ → l’API renvoie 200 OK mais avec une liste vide, car aucun logement ne correspond.

### User diagramme 

![alt text](<User Sequence Diagrams.png>)

## Explications

- Validation des données : vérifie que le nom, l’email et le mot de passe sont valides.
→ 400 Bad Request si les données sont incorrectes (ex. email mal formaté, mot de passe trop court).

- Vérification d’unicité de l’email : avant la création, le système vérifie si l’email est déjà utilisé.
→ 409 Conflict si l’email est déjà enregistré.

- Création de l’utilisateur : si tout est correct, l’utilisateur est sauvegardé en base.
→ 201 Created si la création est réussie + retour de l’objet utilisateur.

**Scénario : Emma souhaite créer un compte sur HBnB.**
### Déroulement technique, étape par étape :

Emma remplit le formulaire d’inscription avec nom, email et mot de passe.
Le client envoie une requête POST /users/register contenant ses informations.
L’API transmet la requête à la couche Business Logic (UserModel) pour valider les données :
Nom non vide.
Email au bon format.
Mot de passe respectant les règles de sécurité.
Si une donnée est invalide → 400 Bad Request avec le message "Invalid data".
Si les données sont valides, le UserModel interroge la base de données pour vérifier si l’email existe déjà.

### Deux cas possibles :

Email déjà utilisé → l’API renvoie 409 Conflict avec le message "Email already registered".
Email libre → un nouvel utilisateur est créé et sauvegardé en base, puis l’API retourne 201 Created avec l’ID utilisateur et un message de succès.

### Exemple concret :

Emma tente de s’inscrire avec un email mal formaté → elle reçoit 400 Bad Request avec "Invalid data".
Emma utilise l’email déjà enregistré "emma@gmail.com
" → elle reçoit 409 Conflict avec "Email already registered".
Emma s’inscrit avec un nouvel email valide → elle reçoit 201 Created, son compte est créé et elle peut se connecter.

---

### conclusion 

- Le document présente une vision claire de l’architecture HBnB.

- La séparation en couches (Presentation, Business Logic, Persistence) garantit la maintenabilité et la modularité.

- Les diagrammes de classes et de séquence assurent une compréhension fine des interactions.

- La présence de la façade (HBNB_Facade) simplifie les interactions et centralise les opérations.

