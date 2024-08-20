from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional

class CreateAdminBody(BaseModel):
    admin_name: str
    email: EmailStr
    password_hash: str

    class Config:
        arbitrary_types_allowed = True

class UpdateAdminBody(BaseModel):
    admin_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
