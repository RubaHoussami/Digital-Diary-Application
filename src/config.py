import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()

        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://username:password@localhost:5432/mydatabase')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        self.SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

def get_config():
    return Config()