import pytest
from pydantic import ValidationError
from src.modules.company.company_dtos import CreateCompanyBody, UpdateCompanyBody  # Adjust the import path based on your project structure

def test_create_company_body_valid():
    data = {
        "company_name": "Test Company",
        "company_description": "This is a test company",
        "company_email": "test@example.com",
        "company_contact_info": "123 Test St",
        "company_payment_options": ["credit", "paypal"]
    }
    body = CreateCompanyBody(**data)
    assert body.company_name == "Test Company"
    assert body.company_email == "test@example.com"

def test_create_company_body_invalid():
    data = {
        "company_name": "Test Company",
        "company_description": "This is a test company",
        "company_email": "invalid-email",  # Invalid email format
        "company_contact_info": "123 Test St",
        "company_payment_options": ["credit", "paypal"]
    }
    with pytest.raises(ValidationError):
        CreateCompanyBody(**data)

def test_update_company_body():
    data = {
        "company_name": "Updated Company",
        "company_email": "updated@example.com"
    }
    body = UpdateCompanyBody(**data)
    assert body.company_name == "Updated Company"
    assert body.company_email == "updated@example.com"
