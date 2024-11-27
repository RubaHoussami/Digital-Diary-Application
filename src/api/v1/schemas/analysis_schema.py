from marshmallow import Schema, fields

class GetAnalysisSchema(Schema):
    id = fields.Int(required=True)
