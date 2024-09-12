from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateAdminBody(BaseModel):
    admin_name: str
    email: EmailStr
    password: str

    class Config:
        arbitrary_types_allowed = True

class UpdateAdminBody(BaseModel):
    admin_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
