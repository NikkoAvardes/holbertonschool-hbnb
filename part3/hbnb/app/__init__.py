"""Initialisation du module principal Flask et de l'API RESTx 
pour l'application HBnB.
"""
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app import config

# Import des namespaces (routes)
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns

# Initialiser le gestionnaire JWT sans application pour l'instant
jwt = JWTManager()


def create_app(config_name='default'):
    """
    Crée et configure l'application Flask avec l'API RESTx et les 
    namespaces nécessaires.
    Retourne l'application Flask prête à être lancée.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
   
    # Initialiser le gestionnaire JWT sans application pour l'instant
    jwt.init_app(app)

    # Initialisation de l'API RESTx
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )
    # Enregistrement des namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
