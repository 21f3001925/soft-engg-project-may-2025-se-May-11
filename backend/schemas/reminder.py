# schemas/reminder.py

from marshmallow import Schema, fields


class ReminderSchema(Schema):
    appointment_id = fields.Str(required=True)
    title = fields.Str(required=True)
    location = fields.Str(required=True)
    date_time = fields.Str(required=True)
    email = fields.Email(required=True)


class MsgSchema(Schema):
    message = fields.Str()
