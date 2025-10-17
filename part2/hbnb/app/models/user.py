
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
        
        # Validation des champs requis
        if not first_name or not first_name.strip():
            raise ValueError("First name cannot be empty")
        if not last_name or not last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
            
        # Vérifie la longueur des noms
        if len(first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")
        if len(last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")
            
        # Vérifie le format de l'email
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
            
        # Affecte les attributs
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.is_admin = is_admin  # Par défaut False
