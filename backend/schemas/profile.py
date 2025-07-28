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
