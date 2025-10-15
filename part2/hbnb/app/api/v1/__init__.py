from flask_restx import Api
from flask import Blueprint
from .users import api as users_ns
from .places import api as places_ns
from .reviews import api as reviews_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(
    blueprint,
    title='HBnB REST API',
    version='1.0',
    description='API for HBnB project (users, places, reviews)'
)

api.add_namespace(users_ns)
api.add_namespace(places_ns)
api.add_namespace(reviews_ns)
