from marshmallow import Schema, fields


class ProfileSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    name = fields.Str()
    age = fields.Int(allow_none=True)
    city = fields.Str(allow_none=True)
    country = fields.Str(allow_none=True)
    phone_number = fields.Str(allow_none=True)
    avatar_url = fields.Str(dump_only=True)
    news_categories = fields.Str(allow_none=True)
    topics_liked = fields.Method("get_topics_liked")
    comments_posted = fields.Method("get_comments_posted")
    appointments_missed = fields.Method("get_appointments_missed")
    medications_missed = fields.Method("get_medications_missed")
    total_screentime = fields.Method("get_total_screentime")

    def get_topics_liked(self, obj):
        if obj.senior_citizen:
            return obj.senior_citizen.topics_liked
        return None

    def get_comments_posted(self, obj):
        if obj.senior_citizen:
            return obj.senior_citizen.comments_posted
        return None

    def get_appointments_missed(self, obj):
        if obj.senior_citizen:
            return obj.senior_citizen.appointments_missed
        return None

    def get_medications_missed(self, obj):
        if obj.senior_citizen:
            return obj.senior_citizen.medications_missed
        return None

    def get_total_screentime(self, obj):
        if obj.senior_citizen:
            return obj.senior_citizen.total_screentime
        return None


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True)


class AvatarUploadSchema(Schema):
    file = fields.Raw(type="file", required=False)
