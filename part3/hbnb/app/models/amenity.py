#!/usr/bin/python3
"""Amenity model module."""

from .base_model import BaseModel
from app import db
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with places.

    Amenities are features like Wi-Fi, parking, air conditioning, etc.
    that enhance the guest experience at a place.
    """

    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        """
        Initialize a new Amenity instance.

        Args:
            name (str): Amenity name (max 50 characters, cannot be empty)

        Raises:
            ValueError: If name is empty or exceeds character limit
        """
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if len(name.strip()) > 50:
            raise ValueError("Name must not exceed 50 characters")

        super().__init__()  # Initialise les attributs hérités de BaseModel
        self.name = name.strip()

    @validates('name')
    def validate_name(self, key, value):
        """Validate the name attribute."""
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        if len(value.strip()) > 50:
            raise ValueError("Name must not exceed 50 characters")
        return value.strip()

    def to_dict(self):
        """
        Convert amenity to dictionary representation.

        Returns:
            dict: Dictionary containing amenity id and name
        """
        return {
            "id": self.id,
            "name": self.name
        }
