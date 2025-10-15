from app.persistence.repository import InMemoryRepository
from models import storage
from models.review import Review
from models.user import User
from models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
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
