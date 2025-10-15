"""Initialisation du module principal Flask et de l'API RESTx pour l'application HBnB."""
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

from app.api.v1.amenities import api as amenities_ns


def create_app():
    """
    Crée et configure l'application Flask avec l'API RESTx et les namespaces nécessaires.
    Retourne l'application Flask prête à être lancée.
    """
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, 
    # and amenities will be added later
    return app, api
