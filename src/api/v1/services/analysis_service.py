from flask import BadRequest
from datetime import datetime, timedelta

from src.api.v1.services.user_service import UserService
from src.api.v1.services.data_service import DataService

from src.crew.active.temporal_analyzer import TemporalAnalyzer
from src.crew.active.advisor import Advisor


class AnalysisService():
    def __init__(self, db_session):
        self.db_session = db_session
        self.user_service = UserService(db_session=db_session)
        self.data_service = DataService(db_session=db_session)
        self.temporal_analyzer = TemporalAnalyzer()
        self.advisor = Advisor()
    
    def analyze_week(self, data, user_id):
        user = self.user_service.get_user(user_id)
        week = data['week']
        year = data['year']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(weeks=1)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.data_service.get_week_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.data_service.get_week_characters_by_date_range(start_date, end_date, user_id)
        analysis = self.temporal_analyzer.analyze(emotions, characters)

        return {'analysis': analysis}

    def analyze_month(self, data, user_id):
        user = self.user_service.get_user(user_id)
        month = data['month']
        year = data['year']
        start_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
        end_date = start_date + timedelta(days=31)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.data_service.get_month_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.data_service.get_month_characters_by_date_range(start_date, end_date, user_id)
        analysis = self.temporal_analyzer.analyze(emotions, characters)

        return {'analysis': analysis}

    def analyze_year(self, data, user_id):
        user = self.user_service.get_user(user_id)
        year = data['year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.data_service.get_year_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.data_service.get_year_characters_by_date_range(start_date, end_date, user_id)
        analysis = self.temporal_analyzer.analyze(emotions, characters)

        return {'analysis': analysis}

    def advise_week(self, data, user_id):
        user = self.user_service.get_user(user_id)
        week = data['week']
        year = data['year']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(weeks=1)
                
        if user.created_at > end_date:
            raise BadRequest('User account was created after the requested timeframe.')

        emotions = self.data_service.get_week_emotions_by_date_range(start_date, end_date, user_id)
        characters = self.data_service.get_week_characters_by_date_range(start_date, end_date, user_id)
        events = self.data_service.get_week_events_by_date_range(start_date, end_date, user_id)
        advice = self.advisor.advise(emotions, characters, events)

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
