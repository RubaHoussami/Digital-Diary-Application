from marshmallow import Schema, fields

class GetDataSchema(Schema):
    id = fields.Int(required=True)

class WeekDataSchema(Schema):
    week = fields.Int(required=True, min=1, max=52)
    year = fields.Int(required=True, min=2024, max=2100)

class MonthDataSchema(Schema):
    month = fields.Int(required=True, min=1, max=12)
    year = fields.Int(required=True, min=2024, max=2100)

class YearDataSchema(Schema):
    year = fields.Int(required=True, min=2024, max=2100)
