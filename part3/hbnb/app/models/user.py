#!/usr/bin/python3
"""User model module."""

import re
from .base_model import BaseModel
import flask_bcrypt as bcrypt
from app import db
from sqlalchemy.orm import validates


class User(BaseModel):
    """
    Represents a user in the HBnB application.

    A user can be either a regular user or an admin, and can own places
    and write reviews. All users must have a unique email address.
"""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email,
                 password=None, is_admin=False):
        """
        Initialize a new User instance.

        Args:
            first_name (str): User's first name (max 50 characters)
            last_name (str): User's last name (max 50 characters)
            email (str): User's email address (must be valid format)
            password (str, optional): User's password (will be hashed)
            is_admin (bool, optional): Whether user has admin privileges.
            Defaults to False.

        Raises:
            ValueError: If any required field is empty, too long,
            or email format is invalid
        """
        super().__init__()

        # Validation des champs requis
        if not first_name or not first_name.strip():
            raise ValueError("First name cannot be empty")
        if not last_name or not last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")

        # Vérifie la longueur des noms
        if len(first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")
        if len(last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")

        # Vérifie le format de l'email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

        # Affecte les attributs
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.is_admin = is_admin

        # Hash automatique du password dans le constructeur
        if password:
            self.hash_password(password)

    # sert à enregistrer un mot de passe de façon sécurisée
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # permet de vérifier un mot de passe lors de la connexion
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        """Validate the first_name attribute."""
        if not first_name or not first_name.strip():
            raise ValueError("First name cannot be empty")
        if len(first_name.strip()) > 50:
            raise ValueError("First name must not exceed 50 characters")
        return first_name.strip()

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        """Validate the last_name attribute."""
        if not last_name or not last_name.strip():
            raise ValueError("Last name cannot be empty")
        if len(last_name.strip()) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        return last_name.strip()

    @validates('email')
    def validate_email(self, key, email):
        """Validate the email attribute."""
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")

        # Vérifie le format de l'email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email.strip()):
            raise ValueError("Invalid email format")

        return email.strip().lower()
