#!/usr/bin/python3
# Importe la classe de base commune
from app.models.base_model import BaseModel


# Classe Place : représente un logement ou une location
class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        # Initialise le lieu avec ses attributs principaux
        super().__init__()
        
        # Validation des champs requis
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        
        # Validation du prix
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
            
        # Validation de la latitude
        if not isinstance(latitude, (int, float)) or latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
            
        # Validation de la longitude  
        if not isinstance(longitude, (int, float)) or longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
            
        # Validation du propriétaire
        if not owner:
            raise ValueError("Owner is required")
        
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
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
