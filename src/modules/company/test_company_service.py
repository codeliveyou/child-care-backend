import pytest
from pymongo import MongoClient
from company_service import CompanyService
from company_dtos import CreateCompanyBody, UpdateCompanyBody
from bson.objectid import ObjectId
from constants import Constants

@pytest.fixture(scope='module')
def db():
    # Connect to MongoDB using the provided connection URL
    client = MongoClient(Constants.DATABASE_URL)
    db = client['CC-database']
    
    yield db

    # Cleanup: delete all collections instead of dropping the database
    for collection in db.list_collection_names():
        db[collection].delete_many({})

def test_create_company(db):
    body = CreateCompanyBody(
        company_name="Test Company",
        company_description="This is a test company",
        company_email="test@example.com",
        company_contact_info="123 Test St",
        company_payment_options=["credit", "paypal"]
    )
    company_id = CompanyService.create(body)
    assert company_id is not None


def test_get_all_companies(db):
    companies = CompanyService.get_all()
    assert isinstance(companies, list)

def test_get_one_company(db):
    company = CompanyService.get_all()[0]  # Get the first company
    company_id = company["_id"]
    fetched_company = CompanyService.get_one(company_id)
    assert fetched_company is not None
    assert fetched_company["company_name"] == "Test Company"

def test_update_company(db):
    company = CompanyService.get_all()[0]
    company_id = company["_id"]
    update_body = UpdateCompanyBody(company_name="Updated Company")
    updated_company = CompanyService.update_one(company_id, update_body)
    assert updated_company["company_name"] == "Updated Company"

def test_delete_company(db):
    company = CompanyService.get_all()[0]
    company_id = company["_id"]
    success = CompanyService.delete_one(company_id)
    assert success

def test_delete_all_companies(db):
    success = CompanyService.delete_all()
    assert success
    companies = CompanyService.get_all()
    assert len(companies) == 0
