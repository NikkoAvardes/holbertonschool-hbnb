"""Facade module for business logic operations."""

from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place


class HBnBFacade:
    """
    Facade for business logic operations in the HBnB application.

    Provides a unified interface for all CRUD operations across
    different entities (users, places, reviews, amenities).
    """

    def __init__(self):
        """Initialize repositories for all entities."""
        self.user_repo = UserRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # User operations
    def create_user(self, user_data):
        """
        Create a new user and add it to the repository.

        Args:
            user_data (dict): Dictionary containing user information

        Returns:
            User: The created user object
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id (str): The unique identifier of the user

        Returns:
            User: The user object if found, None otherwise
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address to search for

        Returns:
            User: The user object if found, None otherwise
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users from the repository."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information by their ID."""
        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

    def get_place(self, place_id):
        """Retrieve a place by its ID."""
        return self.place_repo.get(place_id)

    def get_place_by_title(self, title):
        """Retrieve a place by its title."""
        return self.place_repo.get_by_attribute('title', title)

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with id {owner_id} not found")

        # Create place_data copy without owner_id and add owner object
        place_args = place_data.copy()
        place_args.pop('owner_id', None)
        place_args['owner'] = owner

        place = Place(**place_args)
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        rating = review_data.get("rating")
        text = review_data.get("text")

        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)
        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        new_review = Review(text=text, rating=rating,
                            user_id=user_id, place_id=place_id)

        self.review_repo.add(new_review)
        place.add_review(new_review)

        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = [r for r in self.review_repo.get_all()
                   if r.place_id == place_id]
        return reviews

    def update_review(self, review_id, review_data):
        rating = review_data.get('rating')
        if rating is not None and (not
                                   isinstance(rating,
                                              int) or not (1 <= rating <= 5)):
            raise ValueError("Rating must be an integer between 1 and 5")

        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} not found")

        self.review_repo.delete(review_id)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by its name."""
        return self.amenity_repo.get_by_attribute('name', name)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)

        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        if not amenity:
            raise ValueError(f"Amenity with id {amenity_id} not found")

        place.add_amenity(amenity)
        self.place_repo.save(place)
        return place
