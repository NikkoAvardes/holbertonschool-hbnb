
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
        # Vérifie la validité du nom
        if name == "" or len(name) > 50:
            print("Nom invalide")
        self.name = name
