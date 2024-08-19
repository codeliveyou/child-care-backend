# import pytest
# from mongoengine import connect, disconnect
# from company_schema import CompanySchema
# from datetime import datetime

# @pytest.fixture(scope='module')
# def db():
#     # Set up an in-memory test database using mongomock
#     connect('mongoenginetest', host='mongomock://localhost')
#     yield
#     disconnect()

# def test_create_company(db):
#     company = CompanySchema(
#         company_name="Test Company",
#         company_description="This is a test company",
#         company_email="test@example.com",
#         company_contact_info="123 Test St",
#         company_payment_options=["credit", "paypal"],
#         company_code="ABC123"
#     )
#     company.save()
#     assert company.id is not None
#     assert company.company_name == "Test Company"
#     assert company.created_at is not None
#     assert company.updated_at is not None

# def test_find_company(db):
#     company = CompanySchema.objects(company_code="ABC123").first()
#     assert company is not None
#     assert company.company_name == "Test Company"

# def test_update_company(db):
#     company = CompanySchema.objects(company_code="ABC123").first()
#     company.company_name = "Updated Company"
#     company.save()
#     updated_company = CompanySchema.objects(company_code="ABC123").first()
#     assert updated_company.company_name == "Updated Company"

# def test_delete_company(db):
#     company = CompanySchema.objects(company_code="ABC123").first()
#     company.delete()
#     deleted_company = CompanySchema.objects(company_code="ABC123").first()
#     assert deleted_company is None

# def test_validation_error(db):
#     with pytest.raises(Exception):
#         invalid_company = CompanySchema(
#             company_description="Invalid Company",
#             company_email="invalid@example.com",
#             company_contact_info="123 Test St",
#             company_payment_options=["credit", "paypal"],
#             company_code="XYZ789"
#         )
#         invalid_company.save()
