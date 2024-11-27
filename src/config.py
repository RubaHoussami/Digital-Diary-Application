import os
from dotenv import load_dotenv

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    if env == "development":
        return DevelopmentConfig
    elif env == "testing":
        return TestingConfig
    elif env == "production":
        return ProductionConfig
    else:
        return Config