"""Flask application initialization and API setup for HBnB application."""

import os
from flask import Flask, send_from_directory
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application with RESTx API.

    Sets up the main Flask app with API documentation and registers
    all necessary namespaces for different endpoints.

    Returns:
        Flask: Configured Flask application instance ready to run
    """
    # Configure Flask with static folder
    app = Flask(
        __name__,
        static_folder='static',
        static_url_path='/static'
    )
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Routes for serving HTML pages (must be before API)
    @app.route('/')
    @app.route('/index.html')
    def index():
        """Serve the main index page."""
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/login.html')
    def login():
        """Serve the login page."""
        return send_from_directory(app.static_folder, 'login.html')

    @app.route('/place.html')
    def place():
        """Serve the place details page."""
        return send_from_directory(app.static_folder, 'place.html')

    @app.route('/add_review.html')
    def add_review():
        """Serve the add review page."""
        return send_from_directory(app.static_folder, 'add_review.html')
    
    # API configuration
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/doc'
    )

    # Register API namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.protected import api as protected_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')

    return app
