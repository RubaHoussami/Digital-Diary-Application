from src.extensions import db

class Advice(db.Model):
    __tablename__ = "advice"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    advice = db.Column(db.Text, nullable=False)
    week = db.Column(db.Integer, nullable=True)
    month = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="advice", lazy=True)
