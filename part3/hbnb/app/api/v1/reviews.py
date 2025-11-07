from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)'
    ),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'You cannot review your own place')
    def post(self):
        """Register a new review"""
        current_user_id = get_jwt_identity()

        try:
            data = request.get_json()
            place_id = data.get('place_id')

            # Check if the place exists
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            # Check if the user is trying to review their own place
            if place.owner_id == current_user_id:
                return {"error": "You cannot review your own place"}, 400

            # Check if the user has already reviewed this place
            existing_reviews = facade.get_reviews_by_place(place_id)
            for review in existing_reviews:
                if review.user_id == current_user_id:
                    return {
                        "error": "You have already reviewed this place"
                    }, 400

            # Set the user_id to the authenticated user
            data['user_id'] = current_user_id

            new_review = facade.create_review(data)
            return {
                "id": new_review.id,
                "user_id": new_review.user_id,
                "place_id": new_review.place_id,
                "text": new_review.text,
                "rating": new_review.rating
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = get_jwt_identity()

        try:
            # Get the review first to check ownership
            review = facade.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404

            # Check if user is admin or owner of the review
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            if not is_admin and review.user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            data = request.get_json()
            facade.update_review(review_id, data)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Invalid input data"}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()

        try:
            # Get the review first to check ownership
            review = facade.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404

            # Check if user is admin or owner of the review
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            if not is_admin and review.user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            return {"error": "Invalid input data"}, 400
