
# Fichier modèle Review : représente un avis utilisateur
from .place import Place
from .user import User
from .base_model import BaseModel  # Importe la classe de base


# Classe Review : avis laissé par un utilisateur sur un lieu
class Review(BaseModel):
    """
    Représente un avis laissé par un utilisateur sur un lieu.
    """

    def __init__(self, text, rating, place, user):
        # Initialise l'avis avec ses attributs
        super().__init__()
        # Vérifie que le texte n'est pas vide
        if not text:
            raise ValueError("text vide")
        # Vérifie que le rating est un entier entre 1 et 5
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Le rating doit être un entier entre 1 et 5")
        # Vérifie que place et user sont des instances valides
        # (remplacer 'place' et 'user' par les classes réelles)
        if not isinstance(place, Place) or not isinstance(user, User):
            raise ValueError("Les objets 'place' et 'user' doivent être "
                             "des instances valides")
        # Initialise les attributs
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
