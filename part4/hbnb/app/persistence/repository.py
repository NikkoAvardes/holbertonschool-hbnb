"""Repository pattern implementation for data persistence."""
from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    """
    Abstract base class for repository pattern implementation.

    Defines the interface that all concrete repositories must implement
    for consistent data access operations.
    """

    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.

        Args:
            obj: The object to add to the repository
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The unique identifier of the object

        Returns:
            The object if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects from the repository.

        Returns:
            list: List of all objects in the repository
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an object with new data by its ID.

        Args:
            obj_id (str): The unique identifier of the object
            data (dict): Dictionary containing the new data
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object from the repository by its ID.

        Args:
            obj_id (str): The unique identifier of the object
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute value.

        Args:
            attr_name (str): The name of the attribute to search by
            attr_value: The value to search for

        Returns:
            The first object with matching attribute, None if not found
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository pattern.

    Stores objects in a dictionary for quick access during development
    and testing. Data is not persisted between application restarts.
    """

    def __init__(self):
        """Initialize an in-memory repository with a storage dictionary."""
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the in-memory storage.

        Args:
            obj: The object to add (must have an 'id' attribute)
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by its ID from storage."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Return a list of all stored objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object's attributes with the provided data."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete an object from storage by its ID."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve the first object matching a given attribute value."""
        objs = (
            obj for obj in self._storage.values()
            if getattr(obj, attr_name) == attr_value
        )
        return next(objs, None)


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return (self.model.query.filter
                (getattr(self.model, attr_name) == attr_value).first())

    def save(self, obj):
        """
        Save an object to the database.
        
        Args:
            obj: The object to save
        """
        db.session.add(obj)
        db.session.commit()
