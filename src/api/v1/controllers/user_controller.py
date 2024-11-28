from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, Unauthorized

from extensions import db

from src.api.v1.schemas.user_schema import RegisterSchema, LoginSchema
from src.api.v1.services.user_service import UserService


user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('/register', methods=['POST'])
def register():
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
    user_id = get_jwt_identity()
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
    user_id = get_jwt_identity()
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
    user_id = get_jwt_identity()
    user_service = UserService(db_session=db.session)
    try:
        result = user_service.get_user_info(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
