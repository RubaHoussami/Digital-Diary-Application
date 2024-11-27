from extensions import db
from src.api.v1.models.base_model import BaseModel

class EntryModel(BaseModel, db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user = db.relationship("UserModel", back_populates="entries", lazy=True)
    events = db.relationship("EventModel", back_populates="entry", lazy=True)
    emotions = db.relationship("EmotionModel", back_populates="entry", lazy=True)
    character_traits = db.relationship("CharacterTraitModel", back_populates="entry", lazy=True)
