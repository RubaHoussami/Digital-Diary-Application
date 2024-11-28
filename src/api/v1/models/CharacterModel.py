from extensions import db

class CharacterTrait(db.Model):
    __tablename__ = "character_traits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.id"), nullable=False)

    agreableness = db.Column(db.Float, nullable=False, min=0, max=100)
    conscientiousness = db.Column(db.Float, nullable=False, min=0, max=100)
    extraversion = db.Column(db.Float, nullable=False, min=0, max=100)
    neuroticism = db.Column(db.Float, nullable=False, min=0, max=100)
    openness = db.Column(db.Float, nullable=False, min=0, max=100)

    entry = db.relationship("Entry", back_populates="character_traits", lazy=True)

    def to_dict(self):
        return {
            "entry_id": self.entry_id,
            "agreableness": self.agreableness,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "neuroticism": self.neuroticism,
            "openness": self.openness,
        }
