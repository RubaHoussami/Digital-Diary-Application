from werkzeug.exceptions import BadRequest
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

    def get_emotions(self, entry: Entry) -> Emotion:
        emotions = entry.emotions
        if not emotions:
            emotions_map ={
                'love': False,
                'joy': False,
                'sadness': False,
                'anger': False,
                'fear': False,
                'surprise': False
            }
            text = entry.title + '\n' + entry.context
            for i in range(0, len(text), 128):
                if i + 128 < len(text):
                    emotion = self.emotion_extractor.extract(text[i: i + 128])
                elif len(text) - i > 100:
                    emotion = self.emotion_extractor.extract(text[i:])
                else:
                    emotion = None
                if emotion and emotion in emotions_map:
                    emotions_map[emotion] = True
            emotions = Emotion(love=emotions_map['love'], joy=emotions_map['joy'], sadness=emotions_map['sadness'], anger=emotions_map['anger'], fear=emotions_map['fear'], surprise=emotions_map['surprise'], entry=entry)
            self.db_session.add(emotions)
            self.db_session.commit()

        return emotions
    
    def get_characters(self, entry: Entry) -> CharacterTrait:
        characters = entry.character_traits
        if not characters:
            characters_map ={
                'agreableness': 0,
                'conscientiousness': 0,
                'extraversion': 0,
                'neuroticism': 0,
                'openness': 0
            }
            text = entry.title + '\n' + entry.context
            for i in range(0, len(text), 128):
                if i + 128 < len(text):
                    characters_map = self.character_extractor.extract(text[i: i + 128])
                    agreableness = characters_map['agreableness']
                    conscientiousness = characters_map['conscientiousness']
                    extraversion = characters_map['extraversion']
                    neuroticism = characters_map['neuroticism']
                    openness = characters_map['openness']
                elif len(text) - i > 100:
                    characters_map = self.character_extractor.extract(text[i:])
                    agreableness = characters_map['agreableness']
                    conscientiousness = characters_map['conscientiousness']
                    extraversion = characters_map['extraversion']
                    neuroticism = characters_map['neuroticism']
                    openness = characters_map['openness']
                else: 
                    agreableness = 0
                    conscientiousness = 0
                    extraversion = 0
                    neuroticism = 0
                    openness = 0
                characters_map['agreableness'] += agreableness
                characters_map['conscientiousness'] += conscientiousness
                characters_map['extraversion'] += extraversion
                characters_map['neuroticism'] += neuroticism
                characters_map['openness'] += openness
            number = len(text) // 128
            characters_map['agreableness'] = float(characters_map['agreableness']) / number
            characters_map['conscientiousness'] = float(characters_map['conscientiousness']) / number
            characters_map['extraversion'] = float(characters_map['extraversion']) / number
            characters_map['neuroticism'] = float(characters_map['neuroticism']) / number
            characters_map['openness'] = float(characters_map['openness']) / number
            mbti_type = self.character_extractor.get_mbti_type(characters_map)
            characters = CharacterTrait(agreableness=characters_map['agreableness'], conscientiousness=characters_map['conscientiousness'], extraversion=characters_map['extraversion'], neuroticism=characters_map['neuroticism'], openness=characters_map['openness'], mbti_type=mbti_type, entry=entry)
            self.db_session.add(characters)
            self.db_session.commit()

        return characters
    
    def get_events(self, entry: Entry) -> list[Event]:
        events = entry.events
        if not events:
            events = []
            text = entry.title + '\n' + entry.context
            for i in range(0, len(text), 128):
                if i + 128 < len(text):
                    extracted_event = self.event_extractor.extract(text[i: i + 128])
                elif len(text) - i > 100:
                    extracted_event = self.event_extractor.extract(text[i:])
                else:
                    extracted_event = None
                if extracted_event:
                    single_event = Event(characters=extracted_event['characters'], actions=extracted_event['actions'], times=extracted_event['times'], locations=extracted_event['locations'], objects=extracted_event['objects'], subjects=extracted_event['subjects'], adjectives=extracted_event['adjectives'], adverbs=extracted_event['adverbs'], topics=extracted_event['topics'], organizations=extracted_event['organizations'], events=extracted_event['events'], entry=entry)
                    events.append(single_event)
                    self.db_session.add(single_event)
            self.db_session.commit()

        return events

    def get_entry_emotions(self, entry_id: int, user_id: int) -> dict[str, list]:
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        emotions = self.get_emotions(entry)
        emotions_detected = emotions.to_list()
        return {'emotions': emotions_detected}

    def get_entry_characters(self, entry_id: int, user_id: int) -> dict[str, dict[str, float]]:
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        characters = self.get_characters(entry)
        characters_detected = characters.to_dict()
        return {'characters': characters_detected}
    
    def get_entry_mbti(self, entry_id: int, user_id: int) -> dict[str, str]:
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        characters = self.get_characters(entry)
        mbti_type = characters.mbti_type
        return {'mbti_type': mbti_type}

    def get_entry_events(self, entry_id: int, user_id: int) -> dict[str, list[str]]:
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        events = self.get_events(entry)
        events_detected = [event.to_string() for event in events]
        return {'events': events_detected}

    def get_entry_summary(self, entry_id: int, user_id: int) -> dict[str, dict[str, list[str]]]:
        entry = self.entry_service.get_user_entry(entry_id, user_id)
        emotions = self.get_emotions(entry)
        characters = self.get_characters(entry)
        events = self.get_events(entry)
        return {
            'emotions': emotions.to_list(),
            'characters': characters.to_dict(),
            'events': [event.to_string() for event in events]
        }

    def get_entries_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> list[Entry]:
        return Entry.query.filter(Entry.created_at.between(start_date, end_date), Entry.user_id == user_id).all()

    def get_week_emotions_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, list[str]]:
        entries = self.get_entries_by_date_range(start_date, end_date, user_id)

        week_emotions = {day: set() for day in range(1, 8)}

        for entry in entries:
            day_of_week = entry.created_at.isoweekday()
            emotions = self.get_emotions(entry)
            week_emotions[day_of_week].update(emotions.to_list())
        
        for day in week_emotions:
            week_emotions[day] = list(week_emotions[day])
        
        return week_emotions

    def get_month_emotions_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, list[str]]:
        month_emotions = {day: set() for day in range(1, 32)}

        week_start = start_date
        while week_start <= end_date:
            week_end = week_start + timedelta(days=6)

            if week_end > end_date:
                week_end = end_date

            week_emotions = self.get_week_emotions_by_date_range(week_start, week_end, user_id)

            for day, emotions in week_emotions.items():
                actual_day = (week_start + timedelta(days=day - 1)).day
                month_emotions[actual_day].update(emotions)

            week_start = week_end + timedelta(days=1)
        
        for day in month_emotions:
            month_emotions[day] = list(month_emotions[day])

        return month_emotions

    def get_year_emotions_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, dict[int, list[str]]]:
        year_emotions = {month: {day: set() for day in range(1, 32)} for month in range(1, 13)}

        month_start = start_date
        while month_start <= end_date:
            next_month = month_start.month % 12 + 1
            year = month_start.year + (month_start.month // 12)
            month_end = datetime(year, next_month, 1) - timedelta(days=1)

            if month_end > end_date:
                month_end = end_date

            month_emotions = self.get_month_emotions_by_date_range(month_start, month_end, user_id)

            for day, emotions in month_emotions.items():
                year_emotions[month_start.month][day].update(emotions)

            month_start = month_end + timedelta(days=1)
        
        for month in year_emotions:
            for day in year_emotions[month]:
                year_emotions[month][day] = list(year_emotions[month][day])

        return year_emotions

    def get_week_emotions(self, data: dict[str, int], user_id: int) -> dict[int, list[str]]:
        user = self.user_service.get_user(user_id)
        week = data['week']
        year = data['year']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(weeks=1)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_week_emotions_by_date_range(start_date, end_date, user_id)
        return {'emotions': emotions}

    def get_month_emotions(self, data: dict[str, int], user_id: int) -> dict[int, list[str]]:
        user = self.user_service.get_user(user_id)
        month = data['month']
        year = data['year']
        start_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
        end_date = start_date + timedelta(days=31)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_month_emotions_by_date_range(start_date, end_date, user_id)
        return {'emotions': emotions}

    def get_year_emotions(self, data: dict[str, int], user_id: int) -> dict[int, dict[int, list[str]]]:
        user = self.user_service.get_user(user_id)
        year = data['year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_year_emotions_by_date_range(start_date, end_date, user_id)
        return {'emotions': emotions}

    def get_week_characters_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, dict[str, float]]:
        entries = self.get_entries_by_date_range(start_date, end_date, user_id)

        week_characters = {day: {} for day in range(1, 8)}

        for entry in entries:
            day_of_week = entry.created_at.isoweekday()
            characters = self.get_characters(entry)
            week_characters[day_of_week] = characters.to_dict()
        
        for day in week_characters:
            week_characters[day] = characters.to_dict()

        return week_characters

    def get_month_characters_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, dict[str, float]]:
        month_characters = {day: {} for day in range(1, 32)}

        week_start = start_date
        while week_start <= end_date:
            week_end = week_start + timedelta(days=6)

            if week_end > end_date:
                week_end = end_date

            week_characters = self.get_week_characters_by_date_range(week_start, week_end, user_id)

            for day, characters in week_characters.items():
                actual_day = (week_start + timedelta(days=day - 1)).day
                month_characters[actual_day] = characters.to_dict()

            week_start = week_end + timedelta(days=1)

        return month_characters

    def get_year_characters_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, dict[int, dict[str, float]]]:
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
                year_characters[month_start.month][day] = characters.to_dict()

            month_start = month_end + timedelta(days=1)

        return year_characters

    def get_week_characters(self, data: dict[str, int], user_id: int) -> dict[int, dict[str, float]]:
        user = self.user_service.get_user(user_id)
        week = data['week']
        year = data['year']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(weeks=1)
        
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        characters = self.get_week_characters_by_date_range(start_date, end_date, user_id)
        return {'characters': characters}

    def get_month_characters(self, data: dict[str, int], user_id: int) -> dict[int, dict[str, float]]:
        user = self.user_service.get_user(user_id)
        month = data['month']
        year = data['year']
        start_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
        end_date = start_date + timedelta(days=31)
        
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        characters = self.get_month_characters_by_date_range(start_date, end_date, user_id)
        return {'characters': characters}

    def get_year_characters(self, data: dict[str, int], user_id: int) -> dict[int, dict[int, dict[str, float]]]:
        user = self.user_service.get_user(user_id)
        year = data['year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        characters = self.get_year_characters_by_date_range(start_date, end_date, user_id)
        return {'characters': characters}

    def get_week_summary(self, data: dict[str, int], user_id: int) -> dict[str, dict[str, list[str]]]:
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

    def get_month_summary(self, data: dict[str, int], user_id: int) -> dict[str, dict[str, list[str]]]:
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

    def get_year_summary(self, data: dict[str, int], user_id: int) -> dict[str, dict[str, list[str]]]:
        user = self.user_service.get_user(user_id)
        year = data['year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.get_year_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.get_year_characters_by_date_range(start_date, end_date, user_id)

        return {'emotions': emotions, 'characters': characters}

    def get_week_events_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, list[str]]:
        entries = self.get_entries_by_date_range(start_date, end_date, user_id)

        week_events = {day: [] for day in range(1, 8)}

        for entry in entries:
            day_of_week = entry.created_at.isoweekday()
            events = self.get_events(entry)
            week_events[day_of_week].extend([event.to_string() for event in events])

        return week_events

    def get_month_events_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, list[str]]:
        month_events = {day: [] for day in range(1, 32)}

        week_start = start_date
        while week_start <= end_date:
            week_end = week_start + timedelta(days=6)

            if week_end > end_date:
                week_end = end_date

            week_events = self.get_week_events_by_date_range(week_start, week_end, user_id)

            for day, events in week_events.items():
                actual_day = (week_start + timedelta(days=day - 1)).day
                month_events[actual_day].extend([event.to_string() for event in events])

            week_start = week_end + timedelta(days=1)

        return month_events

    def get_year_events_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> dict[int, dict[int, list[str]]]:
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
                year_events[month_start.month][day].extend([event.to_string() for event in events])

            month_start = month_end + timedelta(days=1)

        return year_events
