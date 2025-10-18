#!/usr/bin/python3
"""Amenity model module."""

from .base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with places.

    Amenities are features like Wi-Fi, parking, air conditioning, etc.
    that enhance the guest experience at a place.
    """

    def __init__(self, name):
        """
        Initialize a new Amenity instance.

        Args:
            name (str): Amenity name (max 50 characters, cannot be empty)

        Raises:
            ValueError: If name is empty or exceeds character limit
        """
        super().__init__()

        # Validation du nom
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if len(name.strip()) > 50:
            raise ValueError("Name must not exceed 50 characters")

        self.name = name.strip()

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
