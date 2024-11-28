from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from datetime import datetime

class RegisterSchema(Schema):
    firstname = fields.Str(required=True, validate=validate.Length(min=1))
    lastname = fields.Str(required=True, validate=validate.Length(min=1))
    username = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    date_of_birth = fields.Date(required=True)
    gender = fields.Str(required=True)

    @validates_schema
    def validate_date_of_birth(date_of_birth):
        today = datetime.today().date()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if age < 18:
            raise ValidationError('User must be at least 18 years old.')

class LoginSchema(Schema):
    identifier = fields.Str(validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
