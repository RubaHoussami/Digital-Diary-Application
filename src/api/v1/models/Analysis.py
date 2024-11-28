from extensions import db

class Analysis(db.Model):
    __tablename__ = "analysis"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    type = db.Column(db.String(50), nullable=False)
    analysis = db.Column(db.Text, nullable=False)
    week = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=True)

    user = db.relationship("User", back_populates="analysis", lazy=True)
