#!/usr/bin/python3
"""Review model module."""

from .base_model import BaseModel
from app import db
from sqlalchemy.orm import validates


class Review(BaseModel):
    """
    Represents a review left by a user for a place.

    A review contains text content and a rating from 1-5 stars,
    and must be associated with both a user and a place.
    """
    __tablename__ = 'reviews'

    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False
    )
    place_id = db.Column(
        db.String(36),
        db.ForeignKey('places.id'),
        nullable=False
    )

    def __init__(
            self, text, rating, user=None, place=None,
            user_id=None, place_id=None):
        """
        Initialize a new Review instance.

        Args:
            text (str): Review text content (cannot be empty)
            rating (int): Rating from 1 to 5 stars
            user (User, optional): User object who wrote the review
            place (Place, optional): Place object being reviewed
            user_id (str, optional): ID of the user
            (if user object not provided)
            place_id (str, optional): ID of the place
            (if place object not provided)

        Raises:
            ValueError: If text is empty, rating is invalid,
            or user/place IDs are missing
        """
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

    @validates('text')
    def validate_text(self, key, text):
        """Validate the text attribute."""
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        if len(text.strip()) > 255:
            raise ValueError("Text must not exceed 255 characters")
        return text.strip()

    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate the rating attribute."""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    @validates('user_id')
    def validate_user_id(self, key, user_id):
        """Validate the user_id attribute."""
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        return user_id

    @validates('place_id')
    def validate_place_id(self, key, place_id):
        """Validate the place_id attribute."""
        if not place_id or not place_id.strip():
            raise ValueError("Place ID cannot be empty")
        return place_id
