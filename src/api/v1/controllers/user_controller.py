from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, Unauthorized

from src.extensions import db

from src.api.v1.schemas.user_schema import RegisterSchema, LoginSchema
from src.api.v1.services.user_service import UserService


user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - firstname
            - lastname
            - username
            - email
            - password
            - date_of_birth
            - gender
          properties:
            firstname:
              type: string
              description: The first name of the user.
            lastname:
              type: string
              description: The last name of the user.
            username:
              type: string
              description: The username of the user.
            email:
              type: string
              format: email
              description: The email address of the user.
            password:
              type: string
              description: The password for the user account.
            date_of_birth:
              type: string
              format: date
              description: The date of birth of the user.
            gender:
              type: string
              description: The gender of the user.
    responses:
      201:
        description: User registered successfully
      400:
        description: Validation error
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = RegisterSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_service = UserService(db_session=db.session)
    try:
        result = user_service.register(data)
        return jsonify(result), 201
    except Unauthorized as e:
        return jsonify({'message': str(e)}), 401
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500


@user_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - identifier
            - password
          properties:
            identifier:
              type: string
              description: The username or email of the user.
            password:
              type: string
              description: The password for the user account.
    responses:
      201:
        description: User logged in successfully
      400:
        description: Validation error
      401:
        description: Unauthorized
      404:
        description: User not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = LoginSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_service = UserService(db_session=db.session)
    try:
        result = user_service.login(data)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Unauthorized as e:
        return jsonify({'message': str(e)}), 401
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@user_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    """
    User logout
    ---
    tags:
      - Users
    security:
      - jwt: []
    responses:
      201:
        description: User logged out successfully
      404:
        description: User not found
      500:
        description: Internal server error
    """
    user_id = int(get_jwt_identity())
    user_service = UserService(db_session=db.session)
    try:
        result = user_service.logout(user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh user access token
    ---
    tags:
      - Users
    security:
      - jwt: []
    responses:
      201:
        description: User access token refreshed successfully
      404:
        description: User not found
      500:
        description: Internal server error
    """
    user_id = int(get_jwt_identity())
    user_service = UserService(db_session=db.session)
    try:
        result = user_service.refresh(user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@user_bp.route('/get_user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    """
    Get user information
    ---
    tags:
      - Users
    security:
      - jwt: []
    responses:
      200:
        description: User information retrieved successfully
      404:
        description: User not found
      500:
        description: Internal server error
    """
    user_id = int(get_jwt_identity())
    user_service = UserService(db_session=db.session)
    try:
        result = user_service.get_user_info(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
