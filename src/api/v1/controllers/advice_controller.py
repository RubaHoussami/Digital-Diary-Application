from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from src.extensions import db

from src.api.v1.services.advice_service import AdviceService
from src.api.v1.schemas.advice_schema import GetAdviceSchema, WeekAdviceSchema, MonthAdviceSchema, YearAdviceSchema


advice_bp = Blueprint('advice', __name__, url_prefix='/advice')

@advice_bp.route('/advise_entry', methods=['POST'])
@jwt_required()
def advise_entry():
    """
    Get advice for a specific entry
    ---
    tags:
      - Advice
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
        description: Advice retrieved successfully
      400:
        description: Validation error
      404:
        description: Entry not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    schema = GetAdviceSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = int(get_jwt_identity())
    entry_id = data['id']
    advice_service = AdviceService(db_session=db.session)
    try:
        result = advice_service.advise_entry(entry_id, user_id)
        return jsonify(result), 201
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

# THESE NEED TO BE FIXED
@advice_bp.route('/advise_week', methods=['POST'])
@jwt_required()
def advise_week():
    data = request.get_json()
    schema = WeekAdviceSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    advice_service = AdviceService(db_session=db.session)
    try:
        result = advice_service.advise_week(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@advice_bp.route('/advise_month', methods=['POST'])
@jwt_required()
def advise_month():
    data = request.get_json()
    schema = MonthAdviceSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    advice_service = AdviceService(db_session=db.session)
    try:
        result = advice_service.advise_month(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@advice_bp.route('/advise_year', methods=['POST'])
@jwt_required()
def advise_year():
    data = request.get_json()
    schema = YearAdviceSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = int(get_jwt_identity())
    advice_service = AdviceService(db_session=db.session)
    try:
        result = advice_service.advise_year(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
