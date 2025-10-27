"""Flask application initialization and API setup for HBnB application."""

from flask import Flask
from flask_restx import Api

# Import des blueprints / namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns

def create_app(config_class="config.DevelopmentConfig"):
    """
    Application Factory - crée et configure l’app Flask avec RESTx API.
    
    Args:
        config_class (str or object): Classe de configuration à utiliser.
    
    Returns:
        Flask: Application Flask configurée avec tous les namespaces API.
    """
    # TODO: Créer une instance Flask
    app = Flask(__name__)
    # TODO: Charger la configuration depuis config_class
    app.config.from_object(config_class)
    
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # TODO: Enregistrer les blueprints (API v1, etc.)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')

    # TODO: Retourner l’application Flask
    return app
