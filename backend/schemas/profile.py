from marshmallow import Schema, fields


class ProfileSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    name = fields.Str()
    avatar_url = fields.Str(dump_only=True)
    news_categories = fields.Str(allow_none=True)


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True)


class AvatarUploadSchema(Schema):
    file = fields.Raw(type="file", required=False)


class SeniorSchema(Schema):
    id = fields.Str(attribute="user_id", dump_only=True)
    username = fields.Str()
    email = fields.Str()
    phone = fields.Str(attribute="phone_number")
    name = fields.Str()
    avatar_url = fields.Str()
    age = fields.Int(attribute="senior_citizen.age")
