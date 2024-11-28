from marshmallow import Schema, fields

class WeekAnalysisSchema(Schema):
    week = fields.Int(required=True, min=1, max=52)
    year = fields.Int(required=True, min=2024, max=2100)

class MonthAnalysisSchema(Schema):
    month = fields.Int(required=True, min=1, max=12)
    year = fields.Int(required=True, min=2024, max=2100)

class YearAnalysisSchema(Schema):
    year = fields.Int(required=True, min=2024, max=2100)
