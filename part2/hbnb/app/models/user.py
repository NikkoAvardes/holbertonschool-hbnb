#!/usr/bin/python3
"""User model module."""

import re
from .base_model import BaseModel


class User(BaseModel):
    """
    Represents a user in the HBnB application.

    A user can be either a regular user or an admin, and can own places
    and write reviews. All users must have a unique email address.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User instance.

        Args:
            first_name (str): User's first name (max 50 characters)
            last_name (str): User's last name (max 50 characters)
            email (str): User's email address (must be valid format)
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
