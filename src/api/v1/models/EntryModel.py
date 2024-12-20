from src.extensions import db
from src.api.v1.models.BaseModel import BaseModel

class Entry(BaseModel, db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(300), nullable=False)
    context = db.Column(db.Text, nullable=False)

    user = db.relationship("User", back_populates="entries", lazy=True)
    events = db.relationship("Event", back_populates="entry", lazy=True)
    emotions = db.relationship("Emotion", back_populates="entry", lazy=True)
    character_traits = db.relationship("CharacterTrait", back_populates="entry", lazy=True)
