# 🏠 HBnB – Partie 4 : Frontend Web

Cette quatrième étape du projet HBnB marque l’intégration d’un **client web moderne** à l’application.  
L’objectif principal est d’offrir une interface utilisateur dynamique qui communique directement avec l’API Flask développée lors des phases précédentes.

---

## ✨ Nouveautés de la partie 4

- **Ajout du frontend statique** : pages HTML (accueil, login, détails d’un lieu, ajout d’avis)
- **Affichage dynamique** des logements et des avis grâce à JavaScript (scripts.js)
- **Filtrage client** des places par prix, sans rechargement de page
- **Gestion de l’authentification** via JWT stocké dans les cookies
- **Affichage conditionnel** des boutons et formulaires selon l’état de connexion
- **Design responsive** adapté à tous les écrans
- **Séparation claire** entre API backend et client webdd

---

## 🖥️ Structure du frontend

```
app/static/
├── index.html         # Page d’accueil avec liste des logements
├── login.html         # Page de connexion utilisateur
├── place.html         # Détail d’un logement et avis
├── add_review.html    # Formulaire d’ajout d’avis
├── scripts.js         # Logique JavaScript (API, affichage, validation)
├── styles.css         # Feuille de style principale
├── images/            # Ressources graphiques (logo, icônes, photos)
```

---

## 🚀 Lancement du serveur

1. Active l’environnement virtuel :
   ```bash
   source venv/bin/activate
   ```
2. Lance le backend Flask :
   ```bash
   python3 run.py
   ```
   Accède à l’API sur [http://127.0.0.1:5000](http://127.0.0.1:5000)
   

Pour arrêter le serveur Flask, utilise `CTRL + C` dans le terminal.

---

## 👤 Test d'authentification

Pour tester la connexion sur le site, utilisez l'utilisateur suivant :

- **Email** : `olga.ivanova@example.com`
- **Mot de passe** : `olga1234`

Ces identifiants permettent d'accéder aux fonctionnalités utilisateur du frontend.

---

## Realise par:

- Nicolai
