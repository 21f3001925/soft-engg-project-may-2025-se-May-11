from marshmallow import Schema, fields


class MedicationSchema(Schema):
    name = fields.Str(required=True)
    dosage = fields.Str(required=True)
    time = fields.DateTime(required=True)
    isTaken = fields.Boolean(missing=False)


class MedicationResponseSchema(Schema):
    medication_id = fields.UUID()
    name = fields.Str()
    dosage = fields.Str()
    time = fields.Str()
    isTaken = fields.Boolean()
    senior_id = fields.UUID()


class MedicationAddResponseSchema(Schema):
    message = fields.Str()
    medication_id = fields.UUID()
