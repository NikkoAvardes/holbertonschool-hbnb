#!/usr/bin/python3
import uuid
from datetime import datetime

class BaseModel:
    """
    Classe de base commune à toutes les entités :
    - gère les IDs uniques
    - les timestamps de création et de mise à jour
    """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour le timestamp updated_at"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Met à jour les attributs d’après un dictionnaire de valeurs"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)  # équivalent à self.first_name = "Nina"
        self.save()
