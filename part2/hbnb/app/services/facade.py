from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place


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
        """Retrieve a place by its ID."""
        return self.place_repo.get(place_id)

    def get_place_by_title(self, title):
        """Retrieve a place by its title."""
        return self.place_repo.get_by_attribute('title', title)

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            return None, f"Owner with id {owner_id} not found"
        
        # Create place_data copy without owner_id and add owner object
        place_args = place_data.copy()
        place_args.pop('owner_id', None)  # Remove owner_id
        place_args['owner'] = owner  # Add owner object
        
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
            return {"error": "Invalid user_id or place_id"}, 400

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return {"error": "Rating must be an integer between 1 and 5"}, 400

        new_review = Review(text=text, rating=rating,
                            user_id=user_id, place_id=place_id)

        self.review_repo.add(new_review)

        return new_review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        reviews = [r for r in self.review_repo.get_all() 
                   if r.place_id == place_id]
        return reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        
        self.review_repo.delete(review_id)
        return True

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)
