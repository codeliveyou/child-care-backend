import pytest
from flask import Flask
from src.modules.company.company_controller import company_blueprint

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(company_blueprint, url_prefix='/company')
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_create_company(client):
    response = client.post('/company/', json={
        "company_name": "Test Company",
        "company_description": "This is a test company",
        "company_email": "test@example.com",
        "company_contact_info": "123 Test St",
        "company_payment_options": ["credit", "paypal"]
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "_id" in data

def test_get_companies(client):
    response = client.get('/company/')
    assert response.status_code == 200
    companies = response.get_json()
    assert isinstance(companies, list)

def test_get_company(client):
    response = client.get('/company/')
    companies = response.get_json()
    company_id = companies[0]['_id']
    response = client.get(f'/company/{company_id}')
    assert response.status_code == 200
    company = response.get_json()
    assert company['company_name'] == "Test Company"

def test_update_company(client):
    response = client.get('/company/')
    companies = response.get_json()
    company_id = companies[0]['_id']
    response = client.put(f'/company/{company_id}', json={
        "company_name": "Updated Company"
    })
    assert response.status_code == 200
    updated_company = response.get_json()
    assert updated_company['company_name'] == "Updated Company"

def test_delete_company(client):
    response = client.get('/company/')
    companies = response.get_json()
    company_id = companies[0]['_id']
    response = client.delete(f'/company/{company_id}')
    assert response.status_code == 200
    message = response.get_json()
    assert message['message'] == "Company deleted successfully"

def test_delete_all_companies(client):
    response = client.delete('/company/delete-all')
    assert response.status_code == 200
    message = response.get_json()
    assert message['message'] == "All companies deleted successfully"
