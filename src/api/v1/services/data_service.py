from flask import BadRequest
from datetime import datetime, timedelta

from src.api.v1.models.EmotionModel import Emotion
from src.api.v1.models.CharacterModel import CharacterTrait
from src.api.v1.models.EventModel import Event
from src.api.v1.models.EntryModel import Entry

from src.api.v1.services.entry_service import EntryService
from src.api.v1.services.user_service import UserService

from src.crew.active.emotion_extractor import EmotionExtractor
from src.crew.active.character_extractor import CharacterExtractor
from src.crew.active.event_extractor import EventExtractor


class DataService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.user_service = UserService(db_session=db_session)
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

        return emotions.to_list()
    
    def get_characters(self, entry):
        characters = entry.character_traits
        if not characters:
            characters_map = self.character_extractor.extract(entry['title'], entry['context'])
            characters = CharacterTrait(agreableness=characters_map['agreableness'], conscientiousness=characters_map['conscientiousness'], extraversion=characters_map['extraversion'], neuroticism=characters_map['neuroticism'], openness=characters_map['openness'], entry=entry)
            self.db_session.add(characters)
            self.db_session.commit()

        return characters.to_dict()
    
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

        events_detected = [event.to_dict() for event in events]
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
    
    def get_entries_by_date_range(self, start_date, end_date, user_id):
        return Entry.query.filter(Entry.created_at.between(start_date, end_date), Entry.user_id == user_id).all()
    
    def get_week_emotions_by_date_range(self, start_date, end_date, user_id):
        entries = self.get_entries_by_date_range(start_date, end_date, user_id)

        week_emotions = {day: [] for day in range(1, 8)}

        for entry in entries:
            day_of_week = entry.created_at.isoweekday()
            emotions = self.get_emotions(entry)
            week_emotions[day_of_week].extend(emotions)
        
        return week_emotions
    
    def get_month_emotions_by_date_range(self, start_date, end_date, user_id):
        month_emotions = {day: [] for day in range(1, 32)}

        week_start = start_date
        while week_start <= end_date:
            week_end = week_start + timedelta(days=6)

            if week_end > end_date:
                week_end = end_date

            week_emotions = self.get_week_emotions_by_date_range(week_start, week_end, user_id)

            for day, emotions in week_emotions.items():
                actual_day = (week_start + timedelta(days=day - 1)).day
                month_emotions[actual_day].extend(emotions)

            week_start = week_end + timedelta(days=1)

        return month_emotions
    
    def get_year_emotions_by_date_range(self, start_date, end_date, user_id):
        year_emotions = {month: {day: [] for day in range(1, 32)} for month in range(1, 13)}

        month_start = start_date
        while month_start <= end_date:
            next_month = month_start.month % 12 + 1
            year = month_start.year + (month_start.month // 12)
            month_end = datetime(year, next_month, 1) - timedelta(days=1)

            if month_end > end_date:
                month_end = end_date

            month_emotions = self.get_month_emotions_by_date_range(month_start, month_end, user_id)

            for day, emotions in month_emotions.items():
                year_emotions[month_start.month][day].extend(emotions)

            month_start = month_end + timedelta(days=1)

        return year_emotions

    def get_week_emotions(self, data, user_id):
        user = self.user_service.get_user(user_id)
        week = data['week']
        year = data['year']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(weeks=1)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_week_emotions_by_date_range(start_date, end_date, user_id)
        return {'emotions': emotions}

    def get_month_emotions(self, data, user_id):
        user = self.user_service.get_user(user_id)
        month = data['month']
        year = data['year']
        start_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
        end_date = start_date + timedelta(days=31)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_month_emotions_by_date_range(start_date, end_date, user_id)
        return {'emotions': emotions}

    def get_year_emotions(self, data, user_id):
        user = self.user_service.get_user(user_id)
        year = data['year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_year_emotions_by_date_range(start_date, end_date, user_id)
        return {'emotions': emotions}
        
    def get_week_characters_by_date_range(self, start_date, end_date, user_id):
        entries = self.get_entries_by_date_range(start_date, end_date, user_id)

        week_characters = {day: {} for day in range(1, 8)}

        for entry in entries:
            day_of_week = entry.created_at.isoweekday()
            characters = self.get_characters(entry)
            week_characters[day_of_week] = characters

        return week_characters

    def get_month_characters_by_date_range(self, start_date, end_date, user_id):
        month_characters = {day: {} for day in range(1, 32)}

        week_start = start_date
        while week_start <= end_date:
            week_end = week_start + timedelta(days=6)

            if week_end > end_date:
                week_end = end_date

            week_characters = self.get_week_characters_by_date_range(week_start, week_end, user_id)

            for day, characters in week_characters.items():
                actual_day = (week_start + timedelta(days=day - 1)).day
                month_characters[actual_day] = characters

            week_start = week_end + timedelta(days=1)

        return month_characters

    def get_year_characters_by_date_range(self, start_date, end_date, user_id):
        year_characters = {month: {day: {} for day in range(1, 32)} for month in range(1, 13)}

        month_start = start_date
        while month_start <= end_date:
            next_month = month_start.month % 12 + 1
            year = month_start.year + (month_start.month // 12)
            month_end = datetime(year, next_month, 1) - timedelta(days=1)

            if month_end > end_date:
                month_end = end_date

            month_characters = self.get_month_characters_by_date_range(month_start, month_end, user_id)

            for day, characters in month_characters.items():
                year_characters[month_start.month][day] = characters

            month_start = month_end + timedelta(days=1)

        return year_characters

    def get_week_characters(self, data, user_id):
        user = self.user_service.get_user(user_id)
        week = data['week']
        year = data['year']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(weeks=1)
        
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        characters = self.get_week_characters_by_date_range(start_date, end_date, user_id)
        return {'characters': characters}

    def get_month_characters(self, data, user_id):
        user = self.user_service.get_user(user_id)
        month = data['month']
        year = data['year']
        start_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
        end_date = start_date + timedelta(days=31)
        
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        characters = self.get_month_characters_by_date_range(start_date, end_date, user_id)
        return {'characters': characters}

    def get_year_characters(self, data, user_id):
        user = self.user_service.get_user(user_id)
        year = data['year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        characters = self.get_year_characters_by_date_range(start_date, end_date, user_id)
        return {'characters': characters}
    
    def get_week_summary(self, data, user_id):
        user = self.user_service.get_user(user_id)
        week = data['week']
        year = data['year']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(weeks=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_week_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.get_week_characters_by_date_range(start_date, end_date, user_id)

        return {'emotions': emotions, 'characters': characters}

    def get_month_summary(self, data, user_id):
        user = self.user_service.get_user(user_id)
        month = data['month']
        year = data['year']
        start_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
        end_date = start_date + timedelta(days=31)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_month_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.get_month_characters_by_date_range(start_date, end_date, user_id)

        return {'emotions': emotions, 'characters': characters}

    def get_year_summary(self, data, user_id):
        user = self.user_service.get_user(user_id)
        year = data['year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_year_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.get_year_characters_by_date_range(start_date, end_date, user_id)

        return {'emotions': emotions, 'characters': characters}
    
    def get_week_events_by_date_range(self, start_date, end_date, user_id):
        entries = self.get_entries_by_date_range(start_date, end_date, user_id)

        week_events = {day: [] for day in range(1, 8)}

        for entry in entries:
            day_of_week = entry.created_at.isoweekday()
            events = self.get_events(entry)
            week_events[day_of_week].extend(events)

        return week_events

    def get_month_events_by_date_range(self, start_date, end_date, user_id):
        month_events = {day: [] for day in range(1, 32)}

        week_start = start_date
        while week_start <= end_date:
            week_end = week_start + timedelta(days=6)

            if week_end > end_date:
                week_end = end_date

            week_events = self.get_week_events_by_date_range(week_start, week_end, user_id)

            for day, events in week_events.items():
                actual_day = (week_start + timedelta(days=day - 1)).day
                month_events[actual_day].extend(events)

            week_start = week_end + timedelta(days=1)

        return month_events


    def get_year_events_by_date_range(self, start_date, end_date, user_id):
        year_events = {month: {day: [] for day in range(1, 32)} for month in range(1, 13)}

        month_start = start_date
        while month_start <= end_date:
            next_month = month_start.month % 12 + 1
            year = month_start.year + (month_start.month // 12)
            month_end = datetime(year, next_month, 1) - timedelta(days=1)

            if month_end > end_date:
                month_end = end_date

            month_events = self.get_month_events_by_date_range(month_start, month_end, user_id)

            for day, events in month_events.items():
                year_events[month_start.month][day].extend(events)

            month_start = month_end + timedelta(days=1)

        return year_events