import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/mydatabase')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Spell checker model path
    SPELL_CHECKER_MODEL_PATH = os.getenv('SPELL_CHECKER_MODEL_PATH', '/path/to/spell_checker/models')

    # Secret key for session management or other security features
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

    # Logger configuration
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'app.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

    # Other configurations can be added here as needed

# Example of how to use the config
config = Config()