from marshmallow import Schema, fields


class EmergencyContactSchema(Schema):
    name = fields.Str(required=True)
    relation = fields.Str(required=True)
    phone = fields.Str(required=True)


class EmergencyContactResponseSchema(Schema):
    contact_id = fields.UUID()
    name = fields.Str()
    relation = fields.Str()
    phone = fields.Str()
    senior_id = fields.UUID()


class EmergencyContactAddResponseSchema(Schema):
    message = fields.Str()
    contact_id = fields.UUID()
