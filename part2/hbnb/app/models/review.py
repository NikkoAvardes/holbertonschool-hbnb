
# Fichier modèle Review : représente un avis utilisateur
from .place import Place
from .user import User
from .base_model import BaseModel  # Importe la classe de base


# Classe Review : avis laissé par un utilisateur sur un lieu
class Review(BaseModel):
    def __init__(self, text, rating, user=None, place=None, user_id=None, place_id=None):
        super().__init__()

        # Validation du texte
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
            
        # Validation du rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        # Validation des IDs
        self.user_id = getattr(user, "id", user_id)
        if not self.user_id:
            raise ValueError("User or user_id is required")

        self.place_id = getattr(place, "id", place_id)
        if not self.place_id:
            raise ValueError("Place or place_id is required")

        self.text = text.strip()
        self.rating = rating
