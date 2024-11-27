from marshmallow import Schema, fields

class RegisterEntrySchema(Schema):
    title = fields.Str(required=True)
    context = fields.Str(required=True)

class GetEntryByIDSchema(Schema):
    id = fields.Int(required=True)

class AddToEntrySchema(Schema):
    id = fields.Int(required=True)
    context = fields.Str(required=True)
