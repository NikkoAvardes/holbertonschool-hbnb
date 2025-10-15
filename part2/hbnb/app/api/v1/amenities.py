#!/usr/bin/python3
# Importation des modules nécessaires

# Flask-RESTx pour l'API REST
from flask_restx import Namespace, Resource, fields
# Facade pour la logique métier
from app.services import facade


# Création d'un espace de noms pour les routes liées aux "amenities"
api = Namespace('amenities', description='Amenity operations')


# Définition du modèle Amenity pour la validation des /
# / entrées et la documentation Swagger
amenity_model = api.model(
    'Amenity', {
        'name': fields.String(
            required=True,
            description="Nom de l'amenity"  # Champ obligatoire
        )
    }
)


# Route pour la liste des amenities
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Enregistre une nouvelle amenity"""
        data = api.payload
        if not data or not data.get('name'):
            return {"error": "Name is required"}, 400
        new_amenity = facade.create_amenity(data)
        if new_amenity is None:
            return {"error": "Failed to create amenity"}, 500
        return new_amenity.to_dict, 201
    
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Récupère la liste de toutes les amenities"""
        amenities = facade.get_all_amenities
        if amenities is None:
            amenities = []
        return amenities, 200


# Route pour une amenity spécifique (par son id)
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Récupère les détails d'une amenity par son ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {"error": 'Amenity not found'}, 404
        return amenity, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Met à jour les informations d'une amenity"""
        data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {"error": "Amenity not found"}, 404
        return updated_amenity, 200
