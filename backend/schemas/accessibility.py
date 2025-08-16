from marshmallow import Schema, fields


class AccessibilitySettingsSchema(Schema):
    font_size = fields.Str(allow_none=True)
    theme = fields.Str(allow_none=True)
