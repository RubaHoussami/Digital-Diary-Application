from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.exceptions import NotFound, Unauthorized

from src.api.v1.utils.get_time import get_utc_now

from src.api.v1.models.UserModel import User


class UserService:
    def __init__(self, db_session):
        self.db_session = db_session

    def _get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def _get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def _get_user_by_id(self, id):
        return User.query.filter_by(id=id).first()

    def get_user_by_username(self, username):
        user = self._get_user_by_username(username)
        if not user:
            raise NotFound(f'User with username {username} not found')
        return user
    
    def get_user_by_email(self, email):
        user = self._get_user_by_email(email)
        if not user:
            raise NotFound(f'User with email {email} not found')
        return user
    
    def get_user_by_id(self, id):
        user = self._get_user_by_id(id)
        if not user:
            raise NotFound(f'User with id {id} not found')
        return user

    def register(self, data):
        firstname = data['firstname']
        lastname = data['lastname']
        username = data['username']
        email = data['email']
        password = data['password']
        date_of_birth = data['date_of_birth']
        gender = data['gender']

        if self._get_user_by_username(username):
            raise Unauthorized(f'User with username {username} already exists')
        if self._get_user_by_email(email):
            raise Unauthorized(f'User with email {email} already exists')

        user = User(firstname=firstname, lastname=lastname, username=username, password='', email=email, date_of_birth=date_of_birth, gender=gender)
        user.set_password(password)

        self.db_session.add(user)
        self.db_session.commit()

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {'access': access_token, 'refresh': refresh_token}

    def login(self, data):
        identifier = data['identifier']
        user = self._get_user_by_username(identifier)

        if not user:
            user = self._get_user_by_email(identifier)
        if not user:
            raise NotFound(f'User with identifier {identifier} not found')

        password = data['password']
        if not user.check_password(password):
            raise Unauthorized(f'Invalid password for user with identifier {identifier}')

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {'access': access_token, 'refresh': refresh_token}
    
    def logout(self, user_id):
        user = self.get_user_by_id(user_id)
        user.last_logout = get_utc_now()
        self.db_session.commit()
        return {'message': 'Logout successful'}

    def refresh(self, user_id):
        user = self.get_user_by_id(user_id)
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {'access': access_token, 'refresh': refresh_token}

    def get_user_info(self, user_id):
        user = self.get_user_by_id(user_id)
        data = {
            'firstname': user.firstname,
            'lastname': user.lastname,
            'username': user.username,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender
        }
        return {'data': data}
