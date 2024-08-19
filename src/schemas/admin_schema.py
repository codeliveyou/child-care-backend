import mongoengine as me
from mongoengine_mate import ExtendedDocument


class AdminSchema(ExtendedDocument):
    name = me.StringField(required=True)

    meta = {
        "strict": False,
    }
