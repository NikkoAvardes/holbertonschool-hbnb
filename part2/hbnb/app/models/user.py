
# Fichier modèle User : représente un utilisateur HBnB
from .base_model import BaseModel  # Importe la classe de base


# Classe User : représente un utilisateur HBnB
class User(BaseModel):
    """
    Représente un utilisateur de l'application HBnB.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        # Initialise l'utilisateur avec ses attributs
        super().__init__()
        # Vérifie la longueur des noms
        if len(first_name) > 50 or len(last_name) > 50:
            print("Le prénom ou le nom ne doit pas dépasser 50 caractères.")
        # Vérifie le format de l'email
        if "@" not in email or "." not in email.split("@")[-1]:
            print("Email invalide")
        # Affecte les attributs
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin  # Par défaut False
