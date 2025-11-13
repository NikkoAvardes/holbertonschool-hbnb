#!/usr/bin/python3
"""Place model module."""

from .base_model import BaseModel
from app import db
from sqlalchemy.orm import validates

# Table d'association pour la relation many-to-many Place <-> Amenity
place_amenity = db.Table('place_amenity',
                         db.Column('place_id', db.String(36),
                                   db.ForeignKey('places.id'),
                                   primary_key=True),
                         db.Column('amenity_id', db.String(36),
                                   db.ForeignKey('amenities.id'),
                                   primary_key=True)
                         )


class Place(BaseModel):
    """
    Represents a place/accommodation that can be booked.

    A place belongs to an owner (User) and can have multiple reviews
    and amenities associated with it.
    """
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Foreign key to User
    owner_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Relationships
    reviews = db.relationship(
        'Review',
        backref='place',
        lazy=True,
        cascade='all, delete-orphan'
    )
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

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
        self.owner_id = owner.id

    @validates('title')
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title.strip()) > 100:
            raise ValueError("Title must not exceed 100 characters")
        return title.strip()

    @validates('price')
    def validate_price(self, key, price):
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
        return float(price)

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        if (not isinstance(latitude, (int, float)) or
                latitude < -90 or latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")
        return float(latitude)

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        if (not isinstance(longitude, (int, float)) or
                longitude < -180 or longitude > 180):
            raise ValueError("Longitude must be between -180 and 180")
        return float(longitude)

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
