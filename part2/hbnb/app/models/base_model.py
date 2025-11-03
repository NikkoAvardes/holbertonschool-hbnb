#!/usr/bin/python3
"""Base model module for all entities."""

import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for all entities in the project.

    Provides common functionality including:
    - Unique ID generation
    - Creation and update timestamps
    - Basic update operations
    """

    def __init__(self):
        """Initialize a new BaseModel instance with
        unique ID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update instance attributes from a dictionary.

        Args:
            data (dict): Dictionary containing attribute names
            and values to update
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
