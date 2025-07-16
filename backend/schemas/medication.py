from marshmallow import Schema, fields


class MedicationSchema(Schema):
    name = fields.Str(required=True)
    dosage = fields.Str(required=True)
    time = fields.Str(required=True)
    isTaken = fields.Boolean(missing=False)
    senior_id = fields.Int(required=True)


class MedicationResponseSchema(Schema):
    medication_id = fields.Int()
    name = fields.Str()
    dosage = fields.Str()
    time = fields.Str()
    isTaken = fields.Boolean()
    senior_id = fields.Int()


class MedicationAddResponseSchema(Schema):
    message = fields.Str()
    medication_id = fields.Int()
