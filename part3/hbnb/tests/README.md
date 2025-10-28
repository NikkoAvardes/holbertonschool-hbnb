# Tests pour l'application HBNB

Ce dossier contient tous les tests unitaires pour l'application HBNB.

## Structure des tests

- `test_user_endpoints.py` : Tests pour les endpoints des utilisateurs
- `test_amenity_endpoints.py` : Tests pour les endpoints des équipements
- `test_place_endpoints.py` : Tests pour les endpoints des logements
- `test_review_endpoints.py` : Tests pour les endpoints des avis
- `run_all_tests.py` : Script pour exécuter tous les tests

## Comment exécuter les tests

### Exécuter tous les tests
```bash
cd /path/to/hbnb
python tests/run_all_tests.py
```

### Exécuter un module de tests spécifique
```bash
cd /path/to/hbnb
python -m unittest tests.test_user_endpoints
python -m unittest tests.test_amenity_endpoints
python -m unittest tests.test_place_endpoints
python -m unittest tests.test_review_endpoints
```

### Exécuter avec pytest (si installé)
```bash
cd /path/to/hbnb
pytest tests/ -v
```

### Exécuter un test spécifique
```bash
cd /path/to/hbnb
python -m unittest tests.test_user_endpoints.TestUserEndpoints.test_create_user
```

## Types de tests

### Tests de création (POST)
- Tests de création avec des données valides
- Tests de création avec des données invalides
- Vérification des codes de statut HTTP appropriés

### Tests de lecture (GET)
- Tests de récupération de tous les éléments
- Tests de récupération d'éléments spécifiques

### Tests de validation
- Validation des formats d'email
- Validation des valeurs numériques (prix, coordonnées, notes)
- Validation des champs obligatoires

## Ajout de nouveaux tests

Pour ajouter de nouveaux tests :

1. Créez une nouvelle classe héritant de `unittest.TestCase`
2. Implémentez la méthode `setUp()` pour initialiser l'application de test
3. Créez des méthodes de test commençant par `test_`
4. Utilisez les assertions appropriées (`assertEqual`, `assertNotEqual`, etc.)
5. Ajoutez votre classe de test dans `run_all_tests.py`

## Configuration

Assurez-vous que l'application peut être importée avec :
```python
from app import create_app
```

L'application doit fournir un client de test via `app.test_client()`.