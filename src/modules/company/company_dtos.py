from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CreateCompanyBody(BaseModel):
    company_name: str
    company_description: str
    company_email: EmailStr
    company_contact_info: str
    company_payment_options: List[str]

class UpdateCompanyBody(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    company_email: Optional[EmailStr] = None
    company_contact_info: Optional[str] = None
    company_payment_options: Optional[List[str]] = None
