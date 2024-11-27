from extensions import db
from src.api.v1.models.base_model import BaseModel

class UserModel(BaseModel, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    entries = db.relationship("EntryModel", back_populates="user", lazy=True)
