"""Flask application initialization and API setup for HBnB application."""

from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns
from flask_jwt_extended import JWTManager


bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application with RESTx API.
    
    Sets up the main Flask app with API documentation and registers
    all necessary namespaces for different endpoints.
    
    Returns:
        Flask: Configured Flask application instance ready to run
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )
    
    jwt.init_app(app)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
