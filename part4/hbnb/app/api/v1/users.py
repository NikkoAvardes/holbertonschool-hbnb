"""User API endpoints for HBnB application."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

# Modèle pour la création d'utilisateur (POST) - champs oblig
user_create_model = api.model(
    'UserCreate', {
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

# Modèle pour maj d'utilisateur (PUT) - champs optionnels
user_update_model = api.model(
    'UserUpdate', {
        'first_name': fields.String(
            required=False, description='First name of the user'),
        'last_name': fields.String(
            required=False, description='Last name of the user'),
        'email': fields.String(
            required=False, description='Email of the user'),
        'password': fields.String(
            required=False, description='Password of the user')
    }
)


@api.route('/')
class UserList(Resource):
    """Resource for user list operations (GET, POST)."""

    @api.expect(user_create_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required(optional=True)
    def post(self):
        """
        Register a new user.

        - Normal users can register themselves (no token required)
        - Admins can create any user (requires token with is_admin=True)
        """
        user_data = api.payload
        try:
            # Vérifier si un utilisateur existe déjà avec cet email
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            # Vérifier si un admin est connecté
            current_user_id = get_jwt_identity()
            if current_user_id:
                claims = get_jwt()
                is_admin = claims.get('is_admin', False)
                if is_admin:
                    # Admin = peut créer n'importe quel utilisateur
                    new_user = facade.create_user(user_data)
                    return {
                        'id': new_user.id,
                        'message': 'Admin created a new user'
                    }, 201

            # Sinon, création standard sans admin
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users."""
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
        """Get user details by ID."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """
        Update a user by ID.

        - Normal users can update only their own data (except email/password)
        - Admins can update any user (including email/password)
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        user_data = api.payload

        # Si l'utilisateur n'est pas admin,
        # vérifier qu'il modifie bien son propre compte
        if not is_admin and current_user_id != user_id:
            return {
                'error': 'Unauthorized action'
            }, 403

        # Si admin → peut modifier tout (email, password inclus)
        if is_admin:
            email = user_data.get('email')
            if email:
                existing_user = facade.get_user_by_email(email)
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400

            # Vérifier que l'utilisateur existe
            existing_user = facade.get_user(user_id)
            if not existing_user:
                return {'error': 'User not found'}, 404

            try:
                updated_user = facade.update_user(user_id, user_data)
                return {"message": "User successfully updated by admin"}, 200
            except ValueError as e:
                return {'error': str(e)}, 400
            except Exception:
                return {'error': 'Invalid input data'}, 400

        # Si utilisateur normal → ne peut pas modifier email ni password
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400

        # Vérifier que l'utilisateur existe
        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404

        try:
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
