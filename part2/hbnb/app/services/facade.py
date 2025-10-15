from app.persistence.repository import InMemoryRepository
from app.models.user import User


class HBnBFacade:
    """Facade for business logic operations in the HBnB application."""
    def __init__(self):
        """Initialize repositories for all entities."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user and add it to the repository."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by their ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by their email address."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users from the repository."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information by their ID."""
        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

    def get_place(self, place_id):
        """Retrieve a place by its ID (to be implemented)."""
        # Logic will be implemented in later tasks
        pass
