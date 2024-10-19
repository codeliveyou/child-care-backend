from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from pydantic import field_validator

class RegisterUserBody(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str
    company_code: str
    account_description: Optional[str] = None
    profile_picture: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class UpdateUserBody(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_password_hash: Optional[str] = None
    user_company_id: Optional[ObjectId] = None
    user_role: Optional[str] = None
    profile_picture: Optional[str] = None  # New field for profile picture

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('user_company_id', mode='before')
    def validate_objectid(cls, v):
        if isinstance(v, str):
            try:
                return ObjectId(v)
            except Exception:
                raise ValueError("Invalid ObjectId format")
        return v

