# schemas/appointment.py

from marshmallow import Schema, fields


class AppointmentSchema(Schema):
    title = fields.String(required=True)
    date_time = fields.DateTime(required=True)
    location = fields.String(required=True)
    reminder_time = fields.DateTime(allow_none=True)


class AppointmentResponseSchema(Schema):
    appointment_id = fields.UUID(required=True, dump_only=True)
    title = fields.String(required=True)
    date_time = fields.DateTime(required=True)
    location = fields.String(required=True)
    reminder_time = fields.DateTime(allow_none=True)
    senior_id = fields.UUID(required=True)


class AppointmentAddResponseSchema(Schema):
    message = fields.String(required=True)
    appointment_id = fields.UUID(required=True)
