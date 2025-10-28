from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = facade.get_user_by_email(email)

        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        identity = user.id
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}, 200
