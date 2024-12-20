from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.api.v1.models.BaseModel import BaseModel

class User(BaseModel, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_logout = db.Column(db.DateTime, nullable=True)

    entries = db.relationship("Entry", back_populates="user", lazy=True)
    advice = db.relationship("Advice", back_populates="user", lazy=True)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
