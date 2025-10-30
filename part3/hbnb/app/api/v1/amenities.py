#!/usr/bin/python3
"""Amenity API endpoints for HBnB application."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

# Create namespace for amenity-related routes
api = Namespace('amenities', description='Amenity operations')

# Define Amenity model for input validation and Swagger documentation
amenity_model = api.model(
    'Amenity', {
        'name': fields.String(
            required=True,
            description="Name of the amenity"
        )
    }
)


@api.route('/')
class AmenityList(Resource):
    """Resource for amenity list operations (GET, POST)."""

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new amenity.

        Creates a new amenity with the provided name. Names must be unique
        and cannot be empty.
        """
        data = api.payload
        try:
            if not data or not data.get('name'):
                return {"error": "Name is required"}, 400
            new_amenity = facade.create_amenity(data)
            if new_amenity is None:
                return {"error": "Failed to create amenity"}, 409
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve list of all amenities.

        Returns a list of all available amenities with their IDs and names.
        """
        amenities = facade.get_all_amenities()
        if amenities is None:
            amenities = []
        amenities_dicts = [a.to_dict() for a in amenities]
        return amenities_dicts, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Resource for individual amenity operations (GET, PUT)."""

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID.

        Args:
            amenity_id (str): The unique identifier of the amenity

        Returns:
            dict: Amenity details if found, error message if not found
        """
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {"error": 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """Met à jour les informations d'une amenity"""
        data = api.payload
        if not data or not data.get('name'):
            return {"error": "Name is required"}, 400

        # Debug: vérifier si l'amenity existe avant update
        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {"error": "Amenity not found"}, 404

        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {"error": "Data is invalid"}, 400
        return {"message": "Amenity updated successfully"}, 200

api = Namespace('amenities', description='Amenities operations')


@api.route('/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        """Créer un nouvel amenity (admin uniquement)"""
        current_user = get_jwt_identity()
        
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        name = amenity_data.get('name')

        if facade.get_amenity_by_name(name): 
            return {'error': 'Amenity already exists'}, 400

        # TODO: Créer le nouvel amenity
        new_amenity = facade.create_amenity(amenity_data)
        return new_amenity.to_dict(), 201

@api.route('/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        """Modifier un amenity (admin uniquement)"""
        current_user = get_jwt_identity()
        
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json


        updated_amenity = facade.update_amenity(amenity_id, data)
        return updated_amenity.to_dict(), 200
