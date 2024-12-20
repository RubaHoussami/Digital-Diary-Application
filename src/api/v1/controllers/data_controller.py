from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from src.extensions import db

from src.api.v1.services.data_service import DataService
from src.api.v1.schemas.data_schema import GetDataSchema, WeekDataSchema, MonthDataSchema, YearDataSchema


data_bp = Blueprint('data', __name__, url_prefix='/data')


@data_bp.route('/get_entry_emotions', methods=['POST'])
@jwt_required()
def get_entry_emotions():
    """
    Get emotions for a specific entry
    ---
    tags:
      - Data
    consumes:
      - application/json
    security:
      - jwt: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - id
          properties:
            id:
              type: integer
              description: The ID of the entry.
    responses:
      201:
        description: Emotions retrieved successfully
      400:
        description: Validation error
      404:
        description: Entry not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = GetDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = int(get_jwt_identity())
    entry_id = data['id']
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_entry_emotions(entry_id, user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_entry_characters', methods=['POST'])
@jwt_required()
def get_entry_characters():
    """
    Get emotions for a specific entry
    ---
    tags:
      - Data
    consumes:
      - application/json
    security:
      - jwt: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - id
          properties:
            id:
              type: integer
              description: The ID of the entry.
    responses:
      201:
        description: Characters retrieved successfully
      400:
        description: Validation error
      404:
        description: Entry not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = GetDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = int(get_jwt_identity())
    entry_id = data['id']
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_entry_characters(entry_id, user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_entry_events', methods=['POST'])
@jwt_required()
def get_entry_events():
    """
    Get emotions for a specific entry
    ---
    tags:
      - Data
    consumes:
      - application/json
    security:
      - jwt: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - id
          properties:
            id:
              type: integer
              description: The ID of the entry.
    responses:
      201:
        description: Events retrieved successfully
      400:
        description: Validation error
      404:
        description: Entry not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = GetDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    entry_id = data['id']
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_entry_events(entry_id, user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_entry_summary', methods=['POST'])
@jwt_required()
def get_entry_summary():
    """
    Get emotions for a specific entry
    ---
    tags:
      - Data
    consumes:
      - application/json
    security:
      - jwt: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - id
          properties:
            id:
              type: integer
              description: The ID of the entry.
    responses:
      201:
        description: Summary retrieved successfully
      400:
        description: Validation error
      404:
        description: Entry not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = GetDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = int(get_jwt_identity())
    entry_id = data['id']
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_entry_summary(entry_id, user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_week_emotions', methods=['POST'])
@jwt_required()
def get_week_emotions():
    data = request.get_json()
    schema = WeekDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_week_emotions(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
    
@data_bp.route('/get_week_characters', methods=['POST'])
@jwt_required()
def get_week_characters():
    data = request.get_json()
    schema = WeekDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_week_characters(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_week_summary', methods=['POST'])
@jwt_required()
def get_week_summary():
    data = request.get_json()
    schema = WeekDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_week_summary(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_month_emotions', methods=['POST'])
@jwt_required()
def get_month_emotions():
    data = request.get_json()
    schema = MonthDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_month_emotions(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_month_characters', methods=['POST'])
@jwt_required()
def get_month_characters():
    data = request.get_json()
    schema = MonthDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_month_characters(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_month_summary', methods=['POST'])
@jwt_required()
def get_month_summary():
    data = request.get_json()
    schema = MonthDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_month_summary(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_year_emotions', methods=['POST'])
@jwt_required()
def get_year_emotions():
    data = request.get_json()
    schema = YearDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_year_emotions(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@data_bp.route('/get_year_characters', methods=['POST'])
@jwt_required()
def get_year_characters():
    data = request.get_json()
    schema = YearDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_year_characters(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
    
@data_bp.route('/get_year_summary', methods=['POST'])
@jwt_required()
def get_year_summary():
    data = request.get_json()
    schema = YearDataSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = int(get_jwt_identity())
    data_service = DataService(db_session=db.session)
    try:
        result = data_service.get_year_summary(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
