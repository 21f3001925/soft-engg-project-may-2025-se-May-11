from marshmallow import Schema, fields


class SignupSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)
    phone_number = fields.Str(required=False)


class LoginSchema(Schema):
    # One of username, email, or phone must be provided
    username = fields.Str(required=False)
    email = fields.Email(required=False)
    phone_number = fields.Str(required=False)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    access_token = fields.Str()


class MsgSchema(Schema):
    msg = fields.Str()
