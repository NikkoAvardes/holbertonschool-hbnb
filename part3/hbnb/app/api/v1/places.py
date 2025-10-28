"""Place API endpoints for HBnB application."""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model),
                             description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model),
                           description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    """Resource for place list operations (GET, POST)."""

    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    def post(self):
        """
        Register a new place.

        Creates a new place with the provided details. The owner must exist
        and geographic coordinates must be valid.
        """
        current_user = get_jwt_identity()
        place_data = api.payload

        place_data['owner_id'] = current_user
        try:
            existing_place = facade.get_place_by_title(place_data.get('title'))
            if existing_place:
                return {'error': 'Place already exist'}, 400

            result = facade.create_place(place_data)
            if isinstance(result, tuple):  # Error case
                return {'error': result[1]}, 400
            new_place = result
            return {
                'id': str(new_place.id),
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
            } for place in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Récupérer toutes les commodités disponibles du système
        # et les retourner comme amenities pour cette place
        all_amenities = facade.get_all_amenities()
        amenities_data = [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in all_amenities
        ]

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': amenities_data
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place_data = api.payload

        # Check if place exists and get its details
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Check if the current user is the owner of the place
        if place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            update_place = facade.update_place(place_id, place_data)
            if not update_place:
                return {"error": "Place not found"}, 404
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Invalid input data'}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        result, status = facade.get_reviews_by_place(place_id)
        return result, status

@api.route('/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        """Permet aux admins de modifier un place sans restriction de propriété"""
        current_user = get_jwt_identity()

        # Si le token ne contient pas la clé is_admin, on considère False par défaut
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        # Récupération du place depuis la façade
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Si l'utilisateur n'est pas admin ET n'est pas propriétaire → refus
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # TODO: Mettre ici la logique pour mettre à jour le place
        data = request.json
        updated_place = facade.update_place(place_id, data)
        return updated_place.to_dict(), 200