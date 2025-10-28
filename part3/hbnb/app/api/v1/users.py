"""User API endpoints for HBnB application."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('users', description='User operations')
user_model = api.model(
    'User', {
        'first_name': fields.String(
            required=True, description='First name of the user'),
        'last_name': fields.String(
            required=True, description='Last name of the user'),
        'email': fields.String(
            required=True, description='Email of the user'),
        'password': fields.String(
            required=True, description='Password of the user')
    }
)


@api.route('/')
class UserList(Resource):
    """Resource for user list operations (GET, POST)."""

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user.

        Creates a new user account with unique email validation.
        Returns the created user details with assigned ID.
        """
        user_data = api.payload
        try:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
            # Extract password and hash it before user creation
            password = user_data.pop('password', None)
            if not password:
                return {'error': 'Password is required'}, 400
            # Create user object and hash password
            new_user = facade.create_user(user_data)
            new_user.hash_password(password)
            return {
                'id': new_user.id,
				'message' : 'user successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Get list of all users.

        Returns a list of all registered users with their basic information.
        """
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            } for user in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """Resource for individual user operations (GET, PUT)."""

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID.

        Args:
            user_id (str): The unique identifier of the user

        Returns:
            dict: User details if found, error message if not found
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update a user by ID.

        Args:
            user_id (str): The unique identifier of the user to update

        Returns:
            dict: Updated user details if successful, error message if failed
        """
        user_data = api.payload
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Invalid input data'}, 400

api = Namespace('users', description='User operations')

@api.route('/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        """Créer un nouvel utilisateur (admin uniquement)"""
        current_user = get_jwt_identity()
        
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # TODO: Créer le nouvel utilisateur avec les données reçues
        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201


@api.route('/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        """Modifier un utilisateur (admin uniquement)"""
        current_user = get_jwt_identity()
        
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # TODO: Mettre à jour l’utilisateur
        updated_user = facade.update_user(user_id, data)
        return updated_user.to_dict(), 200


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        """Modifier un utilisateur (admin uniquement)"""
        current_user = get_jwt_identity()
        
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        # TODO: Mettre à jour les informations de l’utilisateur (email, password, etc.)
        updated_user = facade.update_user(user_id, data)
        return updated_user.to_dict(), 200