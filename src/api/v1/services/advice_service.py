from werkzeug.exceptions import BadRequest
from datetime import datetime, timedelta

from src.api.v1.services.user_service import UserService
from src.api.v1.services.data_service import DataService
from src.api.v1.models.Advice import Advice
from src.crew.active.advisor import Advisor


class AdviceService():
    def __init__(self, db_session):
        self.db_session = db_session
        self.user_service = UserService(db_session=db_session)
        self.data_service = DataService(db_session=db_session)
        self.advisor = Advisor()

    def get_advice(self, week, month, year, user_id):
        return Advice(week=week, month=month, year=year, user_id=user_id)

    def advise_entry(self, entry_id, user_id):
        emotions = self.data_service.get_entry_emotions(entry_id, user_id)
        mbti_type = self.data_service.get_entry_mbti(entry_id, user_id)
        events = self.data_service.get_entry_events(entry_id, user_id)
        advice = self.advisor.advise(emotions, mbti_type, events)

        return {'advice': advice}

    def advise_week(self, data, user_id):
        user = self.user_service.get_user(user_id)
        week = data['week']
        year = data['year']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(weeks=1)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')
        
        advice = self.get_advice(week, None, year, user_id)
        if not advice:
            emotions = self.data_service.get_week_emotions_by_date_range(start_date, end_date, user_id)
            characters = self.data_service.get_week_characters_by_date_range(start_date, end_date, user_id)
            events = self.data_service.get_week_events_by_date_range(start_date, end_date, user_id)
            advice = self.advisor.advise(emotions, characters, events)
            advice = Advice(week=week, month=None, year=year, user_id=user_id, advice=advice)
            self.db_session.add(advice)
            self.db_session.commit()

        return {'advice': advice}

    def advise_month(self, data, user_id):
        user = self.user_service.get_user(user_id)
        month = data['month']
        year = data['year']
        start_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
        end_date = start_date + timedelta(days=31)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.data_service.get_month_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.data_service.get_month_characters_by_date_range(start_date, end_date, user_id)
        events = self.data_service.get_month_events_by_date_range(start_date, end_date, user_id)
        advice = self.advisor.advise(emotions, characters, events)

        return {'advice': advice}

    def advise_year(self, data, user_id):
        user = self.user_service.get_user(user_id)
        year = data['year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.data_service.get_year_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.data_service.get_year_characters_by_date_range(start_date, end_date, user_id)
        events = self.data_service.get_year_events_by_date_range(start_date, end_date, user_id)
        advice = self.advisor.advise(emotions, characters, events)

        return {'advice': advice}
