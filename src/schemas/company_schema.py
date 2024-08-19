from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class CompanySchema(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias='id')
    company_name: str
    company_description: str
    company_email: EmailStr
    company_contact_info: str
    company_payment_options: List[str]
    company_code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            ObjectId: lambda x: str(x),
            datetime: lambda v: v.isoformat(),
        }
        allow_population_by_field_name = True

# Optional: MongoDB schema validation (if using MongoDB's validation)
mongo_schema_validation = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["company_name", "company_email", "company_code", "created_at", "updated_at"],
        "properties": {
            "company_name": {"bsonType": "string", "description": "must be a string and is required"},
            "company_description": {"bsonType": "string", "description": "must be a string"},
            "company_email": {"bsonType": "string", "pattern": "^.+@.+$", "description": "must be a string and match the regex pattern"},
            "company_contact_info": {"bsonType": "string", "description": "must be a string"},
            "company_payment_options": {"bsonType": "array", "items": {"bsonType": "string"}, "description": "must be an array of strings"},
            "company_code": {"bsonType": "string", "description": "must be a string and is required"},
            "created_at": {"bsonType": "date", "description": "must be a date and is required"},
            "updated_at": {"bsonType": "date", "description": "must be a date and is required"}
        }
    }
}
