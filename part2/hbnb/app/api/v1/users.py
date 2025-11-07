"""User API endpoints for HBnB application."""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')
user_model = api.model(
    'User', {
        'first_name': fields.String(
            required=True, description='First name of the user'),
        'last_name': fields.String(
            required=True, description='Last name of the user'),
        'email': fields.String(
            required=True, description='Email of the user')
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
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
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
            # Vérifier que l'utilisateur existe
            existing_user = facade.get_user(user_id)
            if not existing_user:
                return {'error': 'User not found'}, 404
            
            updated_user = facade.update_user(user_id, user_data)
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
