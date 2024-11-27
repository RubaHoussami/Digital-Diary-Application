from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound
from extensions import db
from src.api.v1.services.entry_service import EntryService
from src.api.v1.schemas.entry_schema import RegisterEntrySchema, GetEntryByIDSchema, AddToEntrySchema

entry_bp = Blueprint('entry', __name__, url_prefix='/entries')

@entry_bp.route('/register_entry', methods=['POST'])
@jwt_required()
def register_entry():
    data = request.get_json()
    schema = RegisterEntrySchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = get_jwt_identity()
    entry_service = EntryService(db_session=db.session)
    try:
        result = entry_service.register_entry(data, user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@entry_bp.route('/get_entry_by_id', methods=['GET'])
@jwt_required()
def get_entry_by_id():
    data = request.get_json()
    schema = GetEntryByIDSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = get_jwt_identity()
    entry_id = data['id']
    entry_service = EntryService(db_session=db.session)
    try:
        result = entry_service.get_user_entry(entry_id, user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@entry_bp.route('/get_all_entries', methods=['GET'])
@jwt_required()
def get_all_entries():
    user_id = get_jwt_identity()
    entry_service = EntryService(db_session=db.session)
    try:
        result = entry_service.get_all_entries(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@entry_bp.route('/add_to_entry', methods=['POST'])
@jwt_required()
def add_to_entry():
    data = request.get_json()
    schema = AddToEntrySchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = get_jwt_identity()
    entry_id = data['id']
    entry_service = EntryService(db_session=db.session)
    try:
        result = entry_service.add_to_entry(data, entry_id, user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
    
@entry_bp.route('/get_entry_titles', methods=['GET'])
@jwt_required()
def get_entry_titles():
    user_id = get_jwt_identity()
    entry_service = EntryService(db_session=db.session)
    try:
        result = entry_service.get_entry_titles(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
