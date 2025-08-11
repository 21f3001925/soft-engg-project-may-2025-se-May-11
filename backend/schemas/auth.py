from marshmallow import Schema, fields


class SignupSchema(Schema):
    email = fields.Email(required=False)
    password = fields.Str(required=True)
    role = fields.Str(required=True)
    phone_number = fields.Str(required=False)


class LoginSchema(Schema):
    # One of email or phone_number must be provided
    email = fields.Email(required=False)
    phone_number = fields.Str(required=False)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    access_token = fields.Str()


class MsgSchema(Schema):
    msg = fields.Str()
