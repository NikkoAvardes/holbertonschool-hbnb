"""Flask application initialization and API setup for HBnB application."""

from flask import Flask, jsonify
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS


bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application with RESTx API.
    Create and configure the Flask application with RESTx API.

    Sets up the main Flask app with API documentation and registers
    all necessary namespaces for different endpoints.
    Sets up the main Flask app with API documentation and registers
    all necessary namespaces for different endpoints.

    Returns:
        Flask: Configured Flask application instance ready to run
        Flask: Configured Flask application instance ready to run
    """
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config_class)

    CORS(app, origins=["http://localhost:5000",
         "http://127.0.0.1:5000"], supports_credentials=True)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

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

    # ============================================
    # HTML PAGES ROUTES
    # Serve static HTML pages without /static/ in URL
    # ============================================

    @app.route('/')
    @app.route('/index.html')
    def index():
        """Serve the main index page (list of places)."""
        return app.send_static_file('index.html')

    @app.route('/login.html')
    def login():
        """Serve the login page."""
        return app.send_static_file('login.html')

    @app.route('/place.html')
    def place():
        """Serve the place details page."""
        return app.send_static_file('place.html')

    @app.route('/add_review.html')
    def add_review():
        """Serve the add review page."""
        return app.send_static_file('add_review.html')

    # ============================================
    # API INFO ROUTE
    # Provides information about available endpoints
    # ============================================

    @app.route('/api')
    @app.route('/api/')
    def api_info():
        """API information and available endpoints.

        Returns a JSON object with API documentation URL and
        list of available resource endpoints.

        Returns:
            dict: API information including endpoint URLs
        """
        return jsonify({
            'message': 'Welcome to HBnB API',
            'documentation': '/api/v1/',
            'endpoints': {
                'users': '/api/v1/users',
                'places': '/api/v1/places',
                'amenities': '/api/v1/amenities',
                'reviews': '/api/v1/reviews',
                'auth': '/api/v1/auth'
            }
        })

    return app
