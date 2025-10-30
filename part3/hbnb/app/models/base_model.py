#!/usr/bin/python3
"""Base model module for all entities."""

import uuid
from datetime import datetime
from app import db


class BaseModel:
    """
    Base class for all entities in the project.

    Provides common functionality including:
    - Unique ID generation
    - Creation and update timestamps
    - Basic update operations
    """
    __abstract__ = True  # Ne crée pas de table propre pour BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
