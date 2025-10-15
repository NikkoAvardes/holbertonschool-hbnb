from flask import Flask
from flask_restx import Api
from app.api.v1.reviews import api as reviews_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API')

    # Enregistrer le namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
