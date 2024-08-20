from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from pydantic import ConfigDict, field_validator

class CreateStatisticsBody(BaseModel):
    company_id: ObjectId
    user_id: Optional[ObjectId] = None
    time_spent: int
    sessions_count: int
    rooms_count: int

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('company_id', 'user_id', mode='before')
    def validate_objectid(cls, v):
        if isinstance(v, str):
            try:
                return ObjectId(v)
            except Exception:
                raise ValueError("Invalid ObjectId format")
        return v

class UpdateStatisticsBody(BaseModel):
    time_spent: Optional[int] = None
    sessions_count: Optional[int] = None
    rooms_count: Optional[int] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

