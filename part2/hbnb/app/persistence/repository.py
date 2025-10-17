from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class for a repository pattern."""
    @abstractmethod
    def add(self, obj):
        """Add an object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects from the repository."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object with new data by its ID."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object from the repository by its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value."""
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        """Initialize an in-memory repository with a storage dictionary."""
        self._storage = {}

    def add(self, obj):
        """Add an object to the in-memory storage."""
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
