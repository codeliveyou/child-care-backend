from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CreateCompanyBody(BaseModel):
    company_name: str
    company_description: str
    company_email: EmailStr
    company_telephone: str
    company_admin_email: EmailStr
    company_payment_options: List[str]

class UpdateCompanyBody(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    company_email: Optional[EmailStr] = None
    company_telephone: Optional[str] = None
    company_admin_email: Optional[EmailStr] = None
    company_payment_options: Optional[List[str]] = None

class FilterCompanyByAdminEmail(BaseModel):
    company_admin_email: EmailStr
