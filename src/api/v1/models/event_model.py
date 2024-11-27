from sqlalchemy.dialects.postgresql import ARRAY
from extensions import db

class EventModel(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.id"), nullable=False)

    characters = db.Column(ARRAY(db.String), nullable=False, default=list)
    actions = db.Column(ARRAY(db.String), nullable=False, default=list)
    locations = db.Column(ARRAY(db.String), nullable=False, default=list)
    times = db.Column(ARRAY(db.String), nullable=False, default=list)
    objects = db.Column(ARRAY(db.String), nullable=False, default=list)
    subjects = db.Column(ARRAY(db.String), nullable=False, default=list)
    adjectives = db.Column(ARRAY(db.String), nullable=False, default=list)

    entry = db.relationship("EntryModel", back_populates="events", lazy=True)
