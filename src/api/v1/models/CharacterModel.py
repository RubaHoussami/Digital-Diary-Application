from src.extensions import db

class CharacterTrait(db.Model):
    __tablename__ = "character_traits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.id"), nullable=False)

    agreableness = db.Column(db.Float, nullable=False)
    conscientiousness = db.Column(db.Float, nullable=False)
    extraversion = db.Column(db.Float, nullable=False)
    neuroticism = db.Column(db.Float, nullable=False)
    openness = db.Column(db.Float, nullable=False)
    mbti_type = db.Column(db.String(4), nullable=False)

    entry = db.relationship("Entry", back_populates="character_traits", lazy=True)

    def to_dict(self):
        return {
            "agreableness": self.agreableness,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "neuroticism": self.neuroticism,
            "openness": self.openness,
        }
