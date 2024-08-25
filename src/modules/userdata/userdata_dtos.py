from pydantic import BaseModel, validator
from typing import Optional, List
from bson import ObjectId

class CreateUserDataBody(BaseModel):
    data_url: str
    user_id: str
    data_description: str
    data_type: str
    participants: List[str]

    # Validators for single fields (non-list)
    @validator('data_url', 'user_id', pre=True)
    def validate_and_convert_objectid(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId format")
        return str(ObjectId(value))

    # Validator for list fields
    @validator('participants', pre=True, each_item=True)
    def validate_participant_ids(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId format")
        return str(ObjectId(value))

class UpdateUserDataBody(BaseModel):
    data_url: Optional[str] = None
    user_id: Optional[str] = None
    data_description: Optional[str] = None
    data_type: Optional[str] = None
    participants: Optional[List[str]] = None

    @validator('data_url', 'user_id', pre=True)
    def validate_and_convert_objectid(cls, value):
        if value and not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId format")
        if value:
            return str(ObjectId(value))
        return value

    @validator('participants', pre=True, each_item=True)
    def validate_participant_ids(cls, value):
        if value and not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId format")
        return str(ObjectId(value)) if value else value
