from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class CreateUserActivityBody(BaseModel):
    user_id: str  # Expecting user ID as a string to convert to ObjectId later
    login_time: datetime
    logout_time: Optional[datetime] = None  # Initially, it can be None since logout happens later

class UpdateUserActivityBody(BaseModel):
    logout_time: datetime  # For updating with logout time
