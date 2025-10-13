# app/models/amenity.py
from .base_model import BaseModel

class Amenity(BaseModel):
    """
    Représente une commodité (Wi-Fi, Parking, etc.)
    """

    def __init__(self, name):
        super().__init__()
        if name == "" or len(name) > 50:
            print("Nom invalide")
            self.name = name
