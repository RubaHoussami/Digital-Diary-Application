from werkzeug.exceptions import NotFound

from src.api.v1.models.EntryModel import Entry

from src.api.v1.services.user_service import UserService


class EntryService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.user_service = UserService(db_session=db_session)
    
    def get_entry_by_id(self, id, user_id):
        return Entry.query.filter_by(id=id, user_id=user_id).first()
    
    def get_user_entry_by_id(self, entry_id, user_id):
        entry = self.get_entry_by_id(entry_id, user_id)
        if not entry:
            raise NotFound(f'Entry with id {entry_id} not found for user with id {user_id}')
        return entry
    
    def get_user_entry(self, entry_id, user_id):
        entry = self.get_user_entry_by_id(entry_id, user_id)
        entry_data = {
            'id': entry.id,
            'title': entry.title,
            'context': entry.context
        }
        return {'entry': entry_data}

    def get_all_entries(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        entries = [{
            'id': entry.id,
            'title': entry.title,
            'context': entry.context
        } for entry in user.entries]
        return {'entries': entries}

    def register_entry(self, data, user_id):
        title = data['title']
        title = title.strip()
        context = data['context']
        context = context.strip()
        user = self.user_service.get_user_by_id(user_id)
        entry = Entry(title=title, context=context, user=user)
        self.db_session.add(entry)
        self.db_session.commit()
        return {'id': entry.id}

    def add_to_entry(self, data, entry_id, user_id):
        context = data['context']
        context = context.strip()
        entry = self.get_user_entry_by_id(entry_id, user_id)
        entry.context += context
        self.db_session.commit()
        return {'message': 'Entry updated successfully'}

    def get_entry_titles(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        return {'titles': [entry.title for entry in user.entries]}
