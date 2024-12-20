from src.extensions import db

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

    def to_list(self):
        emotions_list = []
        if self.love:
            emotions_list.append("love")
        if self.joy:
            emotions_list.append("joy")
        if self.sadness:
            emotions_list.append("sadness")
        if self.anger:
            emotions_list.append("anger")
        if self.fear:
            emotions_list.append("fear")
        if self.surprise:
            emotions_list.append("surprise")
        return emotions_list
