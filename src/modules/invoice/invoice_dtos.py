from pydantic import BaseModel, validator
from typing import Optional
from bson import ObjectId

class CreateInvoiceBody(BaseModel):
    company_id: str
    amount: float
    status: str

    @validator('company_id', pre=True)
    def validate_and_convert_company_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId format")
        return str(ObjectId(value))

class UpdateInvoiceBody(BaseModel):
    company_id: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None

    @validator('company_id', pre=True)
    def validate_and_convert_company_id(cls, value):
        if value and not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId format")
        if value:
            return str(ObjectId(value))
        return value
