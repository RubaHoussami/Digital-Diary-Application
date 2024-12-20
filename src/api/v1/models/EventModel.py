from sqlalchemy.dialects.postgresql import ARRAY
from src.extensions import db

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.id"), nullable=False)

    characters = db.Column(ARRAY(db.String), nullable=False, default=list)
    actions = db.Column(ARRAY(db.String), nullable=False, default=list)
    times = db.Column(ARRAY(db.String), nullable=False, default=list)
    locations = db.Column(ARRAY(db.String), nullable=False, default=list)
    objects = db.Column(ARRAY(db.String), nullable=False, default=list)
    subjects = db.Column(ARRAY(db.String), nullable=False, default=list)
    adjectives = db.Column(ARRAY(db.String), nullable=False, default=list)
    adverbs = db.Column(ARRAY(db.String), nullable=False, default=list)
    topics  = db.Column(ARRAY(db.String), nullable=False, default=list)
    organizations = db.Column(ARRAY(db.String), nullable=False, default=list)
    events = db.Column(ARRAY(db.String), nullable=False, default=list)

    entry = db.relationship("Entry", back_populates="events", lazy=True)

    def to_dict(self):
        return {
            "entry_id": self.entry_id,
            "characters": self.characters,
            "actions": self.actions,
            "times": self.times,
            "locations": self.locations,
            "objects": self.objects,
            "subjects": self.subjects,
            "adjectives": self.adjectives,
            "adverbs": self.adverbs,
            "topics": self.topics,
            "organizations": self.organizations,
            "events": self.events
        }

    def to_string(self):
        string = ""
        if self.characters:
            string += f"Characters=[{','.join(self.characters)}]"
        if self.actions:
            string += f", Actions=[{','.join(self.actions)}]"
        if self.times:
            string += f", Times=[{','.join(self.times)}]"
        if self.locations:
            string += f", Locations=[{','.join(self.locations)}]"
        if self.objects:
            string += f", Objects=[{','.join(self.objects)}]"
        if self.subjects:
            string += f", Subjects=[{','.join(self.subjects)}]"
        if self.adjectives:
            string += f", Adjectives=[{','.join(self.adjectives)}]"
        if self.adverbs:
            string += f", Adverbs=[{','.join(self.adverbs)}]"
        if self.topics:
            string += f", Topics=[{','.join(self.topics)}]"
        if self.organizations:
            string += f", Organizations=[{','.join(self.organizations)}]"
        if self.events:
            string += f", Events=[{','.join(self.events)}]"
        return string
