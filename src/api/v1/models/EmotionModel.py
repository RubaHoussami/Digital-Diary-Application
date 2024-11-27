from extensions import db

class Emotion(db.Model):
    __tablename__ = "emotions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.id"), nullable=False)
    
    love = db.Column(db.Boolean, default=False, nullable=False)
    joy = db.Column(db.Boolean, default=False, nullable=False)
    sadness = db.Column(db.Boolean, default=False, nullable=False)
    anger = db.Column(db.Boolean, default=False, nullable=False)
    fear = db.Column(db.Boolean, default=False, nullable=False)
    surprise = db.Column(db.Boolean, default=False, nullable=False)

    entry = db.relationship("Entry", back_populates="emotions", lazy=True)
