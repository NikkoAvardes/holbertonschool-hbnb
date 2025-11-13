"""Place API endpoints for HBnB application."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

amenity_link_model = api.model('PlaceAmenityLink', {
    'name': fields.String(required=True,
                          description='Name of the amenity to add')
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

            new_place = facade.create_place(place_data)
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
                'price': place.price
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

        # Récupérer les amenities associées à cette place spécifique
        place_amenities = [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in place.amenities
        ]

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()
        place_data = api.payload

        # Check if place exists and get its details
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Check if user is admin (from JWT claims) or place owner
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        # Validate input data
        if 'title' in place_data:
            if not place_data['title'] or not str(place_data['title']).strip():
                return {'error': 'Title cannot be empty'}, 400
        if 'price' in place_data:
            try:
                price = float(place_data['price'])
                if price <= 0:
                    return {'error': 'Price must be a positive number'}, 400
            except Exception:
                return {'error': 'Price must be a positive number'}, 400
        if 'latitude' in place_data:
            try:
                latitude = float(place_data['latitude'])
                if latitude < -90 or latitude > 90:
                    return {
                        'error': 'Latitude must be between -90 and 90'
                    }, 400
            except Exception:
                return {
                    'error': 'Latitude must be between -90 and 90'
                }, 400
        if 'longitude' in place_data:
            try:
                longitude = float(place_data['longitude'])
                if longitude < -180 or longitude > 180:
                    return {
                        'error': 'Longitude must be between -180 and 180'
                    }, 400
            except Exception:
                return {'error': 'Longitude must be between -180 and 180'}, 400
        if 'owner_id' in place_data:
            owner = facade.get_user(place_data['owner_id'])
            if not owner:
                return {
                    'error': (
                        f"Owner with id {place_data['owner_id']} not found"
                    )
                }, 400

        try:
            update_place = facade.update_place(place_id, place_data)
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
        # Vérifier que la place existe
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews
        ], 200


@api.route('/<place_id>/amenities')
class PlaceAmenityList(Resource):
    @api.response(200, 'List of amenities for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all amenities for a specific place"""
        # Vérifier que place_id est fourni
        if not place_id:
            return {"error": "Place ID is required"}, 400

        # Vérifier que la place existe
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        amenities = [
            {
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities
        ]
        return amenities, 200

    @jwt_required()
    @api.expect(amenity_link_model)
    @api.response(201, 'Amenity successfully added to place')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def post(self, place_id):
        """Add an amenity to a specific place"""
        current_user_id = get_jwt_identity()
        data = api.payload

        # Vérifier que place_id est fourni
        if not place_id:
            return {"error": "Place ID is required"}, 400

        # Vérifier que le nom de l'amenity est fourni
        amenity_name = data.get('name')
        if not amenity_name or not amenity_name.strip():
            return {"error": "Amenity name is required"}, 400

        # Vérifier que la place existe
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Vérifier que l'utilisateur est propriétaire ou admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            # Récupérer ou créer l'amenity par son nom
            amenity = facade.get_amenity_by_name(amenity_name.strip())
            if not amenity:
                # Créer l'amenity si elle n'existe pas
                amenity = facade.create_amenity({'name': amenity_name.strip()})

            if amenity in place.amenities:
                return {
                    "error": (
                        "Amenity is already associated with this place"
                    )
                }, 409

            # Ajouter l'amenity au place
            facade.add_amenity_to_place(place_id, amenity.id)
            return {"message": "Amenity successfully added to place"}, 201
        except ValueError as e:
            return {'error': str(e)}, 400
