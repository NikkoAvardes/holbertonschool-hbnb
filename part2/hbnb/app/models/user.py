# app/models/user.py
from .base_model import BaseModel


class User(BaseModel):
    """
    Représente un utilisateur de l'application HBnB.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        # TODO: valider que first_name et last_name 
        # ne dépassent pas 50 caractères
        if len(first_name) > 50 or len(last_name) > 50:
            print("Le prénom ou le nom ne doit pas dépasser 50 caractères.")
        # TODO: valider le format de l'email
        if "@" not in email or "." not in email.split("@")[-1]:
            print("Email invalide")
        # TODO: définir les attributs correspondants
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        # TODO: initialiser is_admin (par défaut False)
