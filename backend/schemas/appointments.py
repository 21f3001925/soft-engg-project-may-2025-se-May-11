# schemas/appointment.py

from marshmallow import Schema, fields, validate, ValidationError
import bleach


def validate_not_empty_or_xss(value):
    if not value or not value.strip():
        raise ValidationError("Field cannot be empty or just whitespace.")

    if "javascript:" in value.lower():
        raise ValidationError("Potentially malicious content detected.")

    sanitized_value = bleach.clean(value, tags=[], strip=True)
    if value != sanitized_value:
        raise ValidationError("Potentially malicious HTML content detected.")


class AppointmentSchema(Schema):
    title = fields.String(
        required=True,
        validate=[validate.Length(min=1, max=255), validate_not_empty_or_xss],
    )
    date_time = fields.DateTime(required=True)
    location = fields.String(required=True)
    reminder_time = fields.DateTime(allow_none=True)
    senior_id = fields.UUID(allow_none=True)  # Added for caregiver use
    status = fields.String(
        allow_none=True,
        validate=validate.OneOf(["Scheduled", "Completed", "Missed", "Cancelled"]),
    )


class AppointmentResponseSchema(Schema):
    appointment_id = fields.UUID(required=True, dump_only=True)
    title = fields.String(required=True)
    date_time = fields.DateTime(required=True)
    location = fields.String(
        required=True,
        validate=[validate.Length(min=1, max=255), validate_not_empty_or_xss],
    )
    reminder_time = fields.DateTime(allow_none=True)
    senior_id = fields.UUID(required=True)
    status = fields.String(required=True)


class AppointmentAddResponseSchema(Schema):
    message = fields.String(required=True)
    appointment_id = fields.UUID(required=True)


class AppointmentStatusUpdateSchema(Schema):
    status = fields.String(
        required=True,
        validate=validate.OneOf(["Scheduled", "Completed", "Missed", "Cancelled"]),
    )
