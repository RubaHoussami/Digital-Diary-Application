from src.api.v1.models.EmotionModel import Emotion
from src.api.v1.models.CharacterModel import CharacterTrait
from src.api.v1.models.EventModel import Event

from src.api.v1.services.entry_service import EntryService
from src.crew.active.emotion_extractor import EmotionExtractor
from src.crew.active.character_extractor import CharacterExtractor
from src.crew.active.event_extractor import EventExtractor

class AnalysisService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.entry_service = EntryService(db_session=db_session)
        self.emotion_extractor = EmotionExtractor()
        self.character_extractor = CharacterExtractor()
        self.event_extractor = EventExtractor()

    def get_emotions(self, entry):
        emotions = entry.emotions
        if not emotions:
            emotions_map = self.emotion_extractor.extract(entry['title'], entry['context'])
            emotions = Emotion(love=emotions_map['love'], joy=emotions_map['joy'], sadness=emotions_map['sadness'], anger=emotions_map['anger'], fear=emotions_map['fear'], surprise=emotions_map['surprise'], entry=entry)
            self.db_session.add(emotions)
            self.db_session.commit()

        emotions_detected = []
        if emotions.love:
            emotions_detected.append('love')
        if emotions.joy:
            emotions_detected.append('joy')
        if emotions.sadness:
            emotions_detected.append('sadness')
        if emotions.anger:
            emotions_detected.append('anger')
        if emotions.fear:
            emotions_detected.append('fear')
        if emotions.surprise:
            emotions_detected.append('surprise')
        return emotions_detected
    
    def get_characters(self, entry):
        characters = entry.character_traits
        if not characters:
            characters_map = self.character_extractor.extract(entry['title'], entry['context'])
            characters = CharacterTrait(agreableness=characters_map['agreableness'], conscientiousness=characters_map['conscientiousness'], extraversion=characters_map['extraversion'], neuroticism=characters_map['neuroticism'], openness=characters_map['openness'], entry=entry)
            self.db_session.add(characters)
            self.db_session.commit()

        characters_detected = {
            'agreableness': characters.agreableness,
            'conscientiousness': characters.conscientiousness,
            'extraversion': characters.extraversion,
            'neuroticism': characters.neuroticism,
            'openness': characters.openness
        }
        return characters_detected
    
    def get_events(self, entry):
        events = entry.events
        if not events:
            events_map = self.event_extractor.extract(entry['title'], entry['context'])
            events = []
            for event in events_map:
                single_event = Event(characters=event['characters'], actions=event['actions'], locations=event['locations'], times=event['times'], objects=event['objects'], subjects=event['subjects'], adjectives=event['adjectives'], entry=entry)
                events.append(single_event)
                self.db_session.add(single_event)
            self.db_session.commit()

        events_detected = [{
            'characters': event.characters,
            'actions': event.actions,
            'locations': event.locations,
            'times': event.times,
            'objects': event.objects,
            'subjects': event.subjects,
            'adjectives': event.adjectives
        } for event in events]
        return events_detected
    
    def get_entry_emotions(self, entry_id, user_id):
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        emotions_detected = self.get_emotions(entry)
        return {'emotions': emotions_detected}

    def get_entry_characters(self, entry_id, user_id):
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        characters_detected = self.get_characters(entry)
        return {'characters': characters_detected}

    def get_entry_events(self, entry_id, user_id):
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        events_detected = self.get_events(entry)
        return {'events': events_detected}

    def get_entry_summary(self, entry_id, user_id):
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        emotions_detected = self.get_emotions(entry)
        characters_detected = self.get_characters(entry)
        events_detected = self.get_events(entry)
        return {
            'emotions': emotions_detected,
            'characters': characters_detected,
            'events': events_detected
        }


