from pydantic import BaseModel, Field, validator
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class CreateRoomBody(BaseModel):
    user_id: str
    meeting_title: str
    meeting_description: str
    start_time: datetime
    end_time: datetime
    participants: List[str]

    @validator('user_id', pre=True)
    def validate_and_convert_user_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId format")
        return str(ObjectId(value))

    @validator('participants', each_item=True, pre=True)
    def validate_and_convert_participants(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId format: {value}")
        return str(ObjectId(value))

class UpdateRoomBody(BaseModel):
    meeting_title: Optional[str] = None
    meeting_description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    participants: Optional[List[str]] = None

    @validator('participants', each_item=True, pre=True)
    def validate_and_convert_participants(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId format: {value}")
        return str(ObjectId(value))
