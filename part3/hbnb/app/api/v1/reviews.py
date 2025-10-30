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
            if existing_reviews[1] == 200:  # If successful response
                for review in existing_reviews[0]:
                    if review.get('user_id') == current_user_id:
                        return {"error": "You have already reviewed this place"}, 400

            # Set the user_id to the authenticated user
            data['user_id'] = current_user_id

            result, status = facade.create_review(data)
            return result, status
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        result, status = facade.get_all_reviews()
        return result, status


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        result, status = facade.get_review(review_id)
        return result, status

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
            review_result, review_status = facade.get_review(review_id)
            if review_status != 200:
                return review_result, review_status

            # Check if user is admin or owner of the review
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            if not is_admin and review_result.get('user_id') != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            data = request.get_json()
            result, status = facade.update_review(review_id, data)
            return result, status
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
            review_result, review_status = facade.get_review(review_id)
            if review_status != 200:
                return review_result, review_status

            # Check if user is admin or owner of the review
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            if not is_admin and review_result.get('user_id') != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            result, status = facade.delete_review(review_id)
            return result, status
        except Exception as e:
            return {"error": "Invalid input data"}, 400
