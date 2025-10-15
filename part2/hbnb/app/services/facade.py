from app.persistence.repository import InMemoryRepository
from app.models.user import User

from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from app.models.amenity import Amenity


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

    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        rating = review_data.get("rating")
        text = review_data.get("text")

        user = storage.get(User, user_id)
        place = storage.get(Place, place_id)
        if not user or not place:
            return {"error": "Invalid user_id or place_id"}, 400

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return {"error": "Rating must be an integer between 1 and 5"}, 400

        new_review = Review(text=text, rating=rating,
                            user_id=user_id, place_id=place_id)

        storage.new(new_review)
        storage.save()

        return new_review.to_dict(), 201


    def get_review(self, review_id):
        review = storage.get(Review, review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200


    def get_all_reviews(self):
        reviews = storage.all(Review).values()
        return [r.to_dict() for r in reviews], 200


    def get_reviews_by_place(self, place_id):
        place = storage.get(Place, place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = [r.to_dict() for r in storage.all(Review).values()
                   if r.place_id == place_id]
        return reviews, 200


    def update_review(self, review_id, review_data):
        review = storage.get(Review, review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if "text" in review_data:
            review.text = review_data["text"]

        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return {"error": "Rating must be between 1 and 5"}, 400
            review.rating = rating

        storage.save()
        return {"message": "Review updated successfully"}, 200


    def delete_review(self, review_id):
        review = storage.get(Review, review_id)
        if not review:
            return {"error": "Review not found"}, 404

        storage.delete(review)
        storage.save()
        return {"message": "Review deleted successfully"}, 200

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity.to_dict(), 201
    
    def get_amenity(self, amenity_id):
        # Logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        return self.amenity_repo.update(amenity_id, amenity_data)
