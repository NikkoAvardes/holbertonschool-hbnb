
# Modèle Amenity : représente une commodité (ex : Wi-Fi)
from .base_model import BaseModel  # Importe la classe de base


# Classe pour une commodité (hérite de BaseModel)
class Amenity(BaseModel):
    """
    Représente une commodité (Wi-Fi, Parking, etc.)
    """

    def __init__(self, name):
        # Initialise la commodité avec un nom
        super().__init__()
        
        # Validation du nom
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if len(name.strip()) > 50:
            raise ValueError("Name must not exceed 50 characters")
            
        self.name = name.strip()

    def to_dict(self):
        """Retourne un dictionnaire représentant l'objet Amenity."""
        return {
            "id": self.id,
            "name": self.name
        }
