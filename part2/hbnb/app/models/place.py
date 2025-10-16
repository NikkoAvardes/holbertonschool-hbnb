#!/usr/bin/python3
# Importe la classe de base commune
from app.models.base_model import BaseModel


# Classe Place : représente un logement ou une location
class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        # Initialise le lieu avec ses attributs principaux
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.owner_id = owner.id  # Store owner ID for easy access
        # Liste des avis associés au lieu
        self.reviews = []
        # Liste des commodités associées au lieu
        self.amenities = []

    def add_review(self, review):
        # Ajoute un avis au lieu
        self.reviews.append(review)

    def add_amenity(self, amenity):
        # Ajoute une commodité au lieu
        self.amenities.append(amenity)
