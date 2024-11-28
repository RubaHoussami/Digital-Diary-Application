from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from extensions import db

from src.api.v1.services.analysis_service import AnalysisService
from src.api.v1.schemas.analysis_schema import WeekAnalysisSchema, MonthAnalysisSchema, YearAnalysisSchema


analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_bp.route('/analyze_week', methods=['POST'])
@jwt_required()
def analyze_week():
    data = request.get_json()
    schema = WeekAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.analyze_week(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/analyze_month', methods=['POST'])
@jwt_required()
def analyze_month():
    data = request.get_json()
    schema = MonthAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.analyze_month(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/analyze_year', methods=['POST'])
@jwt_required()
def analyze_year():
    data = request.get_json()
    schema = YearAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.analyze_year(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/advise_week', methods=['POST'])
@jwt_required()
def advise_week():
    data = request.get_json()
    schema = WeekAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.advise_week(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/advise_month', methods=['POST'])
@jwt_required()
def advise_month():
    data = request.get_json()
    schema = MonthAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.advise_month(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/advise_year', methods=['POST'])
@jwt_required()
def advise_year():
    data = request.get_json()
    schema = YearAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400

    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.advise_year(data, user_id)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
