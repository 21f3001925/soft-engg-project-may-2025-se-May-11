from marshmallow import Schema, fields


class ReportSchema(Schema):
    report_id = fields.UUID(dump_only=True)
    original_filename = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    summary = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
