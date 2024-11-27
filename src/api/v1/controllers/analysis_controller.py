from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError
from extensions import db
from src.api.v1.services.analysis_service import AnalysisService
from src.api.v1.schemas.analysis_schema import GetAnalysisSchema

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_bp.route('/get_entry_emotions', methods=['POST'])
@jwt_required()
def get_entry_emotions():
    data = request.get_json()
    schema = GetAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = get_jwt_identity()
    entry_id = data['id']
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_entry_emotions(entry_id, user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/get_entry_characters', methods=['POST'])
@jwt_required()
def get_entry_characters():
    data = request.get_json()
    schema = GetAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = get_jwt_identity()
    entry_id = data['id']
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_entry_characters(entry_id, user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
    
@analysis_bp.route('/get_entry_events', methods=['POST'])
@jwt_required()
def get_entry_events():
    data = request.get_json()
    schema = GetAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = get_jwt_identity()
    entry_id = data['id']
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_entry_events(entry_id, user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/get_entry_summary', methods=['POST'])
@jwt_required()
def get_entry_summary():
    data = request.get_json()
    schema = GetAnalysisSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({'message': f'Validation error: {e.messages}'}), 400
    
    user_id = get_jwt_identity()
    entry_id = data['id']
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_entry_summary(entry_id, user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/get_week_emotions', methods=['POST'])
@jwt_required()
def get_week_emotions():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_week_emotions(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
    
@analysis_bp.route('/get_month_emotions', methods=['POST'])
@jwt_required()
def get_month_emotions():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_month_emotions(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/get_year_emotions', methods=['POST'])
@jwt_required()
def get_month_emotions():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_year_emotions(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/get_week_characters', methods=['POST'])
@jwt_required()
def get_week_characters():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_week_characters(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/get_month_characters', methods=['POST'])
@jwt_required()
def get_month_characters():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_month_characters(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/get_year_characters', methods=['POST'])
@jwt_required()
def get_year_characters():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.get_year_characters(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/analyze_week', methods=['POST'])
@jwt_required()
def analyze_week():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.analyze_week(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/analyze_month', methods=['POST'])
@jwt_required()
def analyze_month():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.analyze_month(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@analysis_bp.route('/analyze_year', methods=['POST'])
@jwt_required()
def analyze_year():
    user_id = get_jwt_identity()
    analysis_service = AnalysisService(db_session=db.session)
    try:
        result = analysis_service.analyze_year(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
