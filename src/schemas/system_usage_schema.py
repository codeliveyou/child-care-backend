import mongoengine as me
from mongoengine_mate import ExtendedDocument


class System_usageSchema(ExtendedDocument):
    name = me.StringField(required=True)

    meta = {
        "strict": False,
    }
