#!/usr/bin/python3
"""Place model module."""

from .base_model import BaseModel
from app import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """
    Represents a place/accommodation that can be booked.

    A place belongs to an owner (User) and can have multiple reviews
    and amenities associated with it.
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place instance.

        Args:
            title (str): Place title (cannot be empty)
            description (str): Place description (optional)
            price (float): Price per night (must be positive)
            latitude (float): Geographic latitude (-90 to 90)
            longitude (float): Geographic longitude (-180 to 180)
            owner (User): The user who owns this place

        Raises:
            ValueError: If any validation fails
        """
        super().__init__()

        # Validation des champs requis
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        # Validation du prix
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")

        # Validation de la latitude
        if (not isinstance(latitude, (int, float)) or
                latitude < -90 or latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")

        # Validation de la longitude
        if (not isinstance(longitude, (int, float)) or
                longitude < -180 or longitude > 180):
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
        self.owner_id = owner.id
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """
        Add a review to this place.

        Args:
            review (Review): The review to add
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to this place.

        Args:
            amenity (Amenity): The amenity to add
        """
        self.amenities.append(amenity)
