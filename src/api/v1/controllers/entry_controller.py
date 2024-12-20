from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError
from src.errors import DangerDetected

from src.extensions import db

from src.api.v1.services.entry_service import EntryService
from src.api.v1.schemas.entry_schema import RegisterEntrySchema, GetEntryByIDSchema, AddToEntrySchema


entry_bp = Blueprint('entry', __name__, url_prefix='/entries')


@entry_bp.route('/register_entry', methods=['POST'])
@jwt_required()
def register_entry():
    """
    Register a new entry
    ---
    tags:
      - Entries
    consumes:
      - application/json
    security:
      - jwt: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
              description: The title of the entry.
            context:
              type: string
              description: The context or content of the entry.
    responses:
      201:
        description: Entry registered successfully
      400:
        description: Validation error
      404:
        description: Entry not found
      405:
        description: Danger detected
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = RegisterEntrySchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    entry_service = EntryService(db_session=db.session)
    try:
        result = entry_service.register_entry(data, user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except DangerDetected as e:
        return jsonify({'message': str(e)}), 405
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@entry_bp.route('/get_entry_by_id', methods=['POST'])
@jwt_required()
def get_entry_by_id():
    """
    Get an entry by ID
    ---
    tags:
      - Entries
    consumes:
      - application/json
    security:
      - jwt: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            id:
              type: integer
              description: The ID of the entry to retrieve.
    responses:
      200:
        description: Entry retrieved successfully
      400:
        description: Validation error
      404:
        description: Entry not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = GetEntryByIDSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
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
    """
    Get all entries
    ---
    tags:
      - Entries
    security:
      - jwt: []
    responses:
      200:
        description: Entries retrieved successfully
      404:
        description: Entries not found
      500:
        description: Internal server error
    """
    user_id = int(get_jwt_identity())
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
    """
    Add context to an existing entry
    ---
    tags:
      - Entries
    consumes:
      - application/json
    security:
      - jwt: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            id:
              type: integer
              description: The ID of the entry to update.
            context:
              type: string
              description: The additional context to add to the entry.
    responses:
      201:
        description: Entry updated successfully
      400:
        description: Validation error
      404:
        description: Entry not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = AddToEntrySchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = int(get_jwt_identity())
    entry_id = data['id']
    entry_service = EntryService(db_session=db.session)
    try:
        result = entry_service.add_to_entry(data, entry_id, user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
    
@entry_bp.route('/get_entry_titles', methods=['GET'])
@jwt_required()
def get_entry_titles():
    """
    Get all entry titles
    ---
    tags:
      - Entries
    security:
      - jwt: []
    responses:
      200:
        description: Entry titles retrieved successfully
      404:
        description: Entry not found
      500:
        description: Internal server error
    """
    user_id = int(get_jwt_identity())
    entry_service = EntryService(db_session=db.session)
    try:
        result = entry_service.get_entry_titles(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
