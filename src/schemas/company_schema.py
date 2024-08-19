import mongoengine as me
from mongoengine_mate import ExtendedDocument
from datetime import datetime

class CompanySchema(ExtendedDocument):
    company_name = me.StringField(required=True, max_length=255)
    company_description = me.StringField(required=True)
    company_email = me.EmailField(required=True, unique=True)
    company_contact_info = me.StringField(required=True)
    company_payment_options = me.ListField(me.StringField(), required=True)
    company_code = me.StringField(required=True, unique=True, max_length=6)
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "companies",  # Optional: Specify collection name
        "strict": False,
        "indexes": [
            "company_code",  # Create an index for faster lookups by company_code
            "company_email",  # Ensure email uniqueness is enforced
        ],
    }

    def save(self, *args, **kwargs):
        """Override save method to auto-update `updated_at` field."""
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return super(CompanySchema, self).save(*args, **kwargs)
