from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version="1.0", title="API Example", description="Une API simple avec Flask-RESTX")

ns = api.namespace('hello', description='Exemple simple')

@ns.route('/')
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello, Flask-RESTX!"}

if __name__ == '__main__':
    app.run(debug=True)
