from flask import Flask, jsonify
from src.extensions import swagger
from src.logger import logger
#from src.config import Config

def create_app():
    app = Flask(__name__)
    #config = Config()

    swagger.init_app(app)

    return app

app = create_app()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the Digital Diary App'}), 200


if __name__ == '__main__':
    logger.info('Starting the Digital Diary App')
    app.run(debug=True)
