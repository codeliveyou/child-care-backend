import mongoengine as me
from mongoengine_mate import ExtendedDocument


class Company_activitySchema(ExtendedDocument):
    name = me.StringField(required=True)

    meta = {
        "strict": False,
    }
