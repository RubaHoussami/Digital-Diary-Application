from marshmallow import Schema, fields

class GetAdviceSchema(Schema):
    id = fields.Int(required=True)

class WeekAdviceSchema(Schema):
    week = fields.Int(required=True, min=1, max=52)
    year = fields.Int(required=True, min=2024, max=2100)

class MonthAdviceSchema(Schema):
    month = fields.Int(required=True, min=1, max=12)
    year = fields.Int(required=True, min=2024, max=2100)

class YearAdviceSchema(Schema):
    year = fields.Int(required=True, min=2024, max=2100)
