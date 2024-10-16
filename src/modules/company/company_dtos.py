from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CreateCompanyBody(BaseModel):
    company_name: str
    company_description: str
    company_email: EmailStr
    company_telephone: str  # New field for company telephone
    company_admin_email: EmailStr  # New field for company admin email
    company_payment_options: List[str]

class UpdateCompanyBody(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    company_email: Optional[EmailStr] = None
    company_telephone: Optional[str] = None  # New field for company telephone
    company_admin_email: Optional[EmailStr] = None  # New field for company admin email
    company_payment_options: Optional[List[str]] = None
