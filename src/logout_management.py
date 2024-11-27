from flask import jsonify
from src.extensions import db, jwt
from src.api.v1.services.user_service import UserService

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    user_id = jwt_payload['sub']
    user_service = UserService(db.session)
    user = user_service.get_user_by_id(user_id)
    if user.last_logout:
        return jwt_payload['iat'] < user.last_logout.timestamp()
    return False

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked'}), 401
