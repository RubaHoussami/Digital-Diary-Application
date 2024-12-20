from flask import Flask, jsonify

from src.extensions import db, migrate, jwt, cors, swagger
from src.logger import logger
from src.config import get_config
from src.logout_management import is_token_revoked, revoked_token_callback

from src.api.v1.models.UserModel import User
from src.api.v1.models.EntryModel import Entry
from src.api.v1.models.EventModel import Event
from src.api.v1.models.EmotionModel import Emotion
from src.api.v1.models.CharacterModel import CharacterTrait

from src.api.v1.controllers.user_controller import user_bp
from src.api.v1.controllers.entry_controller import entry_bp
from src.api.v1.controllers.advice_controller import advice_bp
from src.api.v1.controllers.data_controller import data_bp


def create_app():
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    swagger.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(entry_bp)
    app.register_blueprint(advice_bp)
    app.register_blueprint(data_bp)
    return app

app = create_app()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the Digital Diary App'}), 200


if __name__ == '__main__':
    logger.info('Starting the Digital Diary App')
    app.run(debug=True)
