
# Fichier modèle Review : représente un avis utilisateur
from .place import Place
from .user import User
from .base_model import BaseModel  # Importe la classe de base


# Classe Review : avis laissé par un utilisateur sur un lieu
class Review(BaseModel):
    def __init__(self, text, rating, user=None, place=None, user_id=None, place_id=None):
        super().__init__()

        if not text:
            raise ValueError("text vide")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Le rating doit être un entier entre 1 et 5")

        # Accepte soit les objets, soit les IDs
        if user:
            self.user_id = user.id
        elif user_id:
            self.user_id = user_id
        else:
            raise ValueError("user ou user_id requis")

        if place:
            self.place_id = place.id
        elif place_id:
            self.place_id = place_id
        else:
            raise ValueError("place ou place_id requis")

        self.text = text
        self.rating = rating
