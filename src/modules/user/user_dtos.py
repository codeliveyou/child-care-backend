from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from pydantic import field_validator

class RegisterUserBody(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str  # Use plain password
    company_code: str  # The code to associate user with company

    class Config:
        arbitrary_types_allowed = True

    # Validation for other fields can be added here if needed

class CreateUserBody(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password_hash: str  # This holds the hashed password
    user_company_id: Optional[ObjectId]
    user_role: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('user_company_id', mode='before')
    def validate_objectid(cls, v):
        if isinstance(v, str):
            try:
                return ObjectId(v)
            except Exception:
                raise ValueError("Invalid ObjectId format")
        return v

class UpdateUserBody(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_password_hash: Optional[str] = None
    user_company_id: Optional[ObjectId] = None
    user_role: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('user_company_id', mode='before')
    def validate_objectid(cls, v):
        if isinstance(v, str):
            try:
                return ObjectId(v)
            except Exception:
                raise ValueError("Invalid ObjectId format")
        return v
