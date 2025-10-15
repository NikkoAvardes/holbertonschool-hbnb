#!/usr/bin/python3
# Importe uuid pour générer des identifiants uniques
import uuid
# Importe datetime pour gérer les dates
from datetime import datetime


# Classe de base pour tous les modèles du projet
class BaseModel:
    """
    Classe de base commune à toutes les entités :
    - gère les IDs uniques
    - les timestamps de création et de mise à jour
    """

    def __init__(self, name):
        # Initialise l'ID unique et les timestamps
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        # Met à jour le timestamp updated_at
        self.updated_at = datetime.now()

    def update(self, data):
        # Met à jour les attributs à partir d'un dictionnaire
        for key, value in data.items():
            if hasattr(self, key):
                # Affecte la valeur à l'attribut correspondant
                setattr(self, key, value)
        self.save()
