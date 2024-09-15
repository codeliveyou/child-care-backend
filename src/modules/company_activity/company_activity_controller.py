from flask import Blueprint
from flask_pydantic import validate
from src.modules.company_activity.company_activity_service import CompanyActivityService
from src.modules.company_activity.company_activity_dtos import CreateCompany_activityBody, UpdateCompany_activityBody
from src.utils.responder import Responder
from flask_pydantic_docs import openapi_docs

company_activity_controller = Blueprint('company_activitys', __name__)


@company_activity_controller.post('/')
@openapi_docs()
@validate()
def create_company_activity(body: CreateCompany_activityBody):
    return CompanyActivityService.create(body)

@company_activity_controller.get('/<id>')
@openapi_docs()
@validate()
def get_one_company_activity(id):
    return CompanyActivityService.get_one(id)

@company_activity_controller.get('/')
@openapi_docs()
@validate()
def get_all_company_activitys():
    return CompanyActivityService.get_all()

@company_activity_controller.put('/<id>')
@openapi_docs()
@validate()
def update_one_company_activity(id, body: UpdateCompany_activityBody):
    return CompanyActivityService.update_one(id, body)

@company_activity_controller.delete('/<id>')
@openapi_docs()
@validate()
def delete_one_company_activity(id):
    return CompanyActivityService.delete_one(id)

@company_activity_controller.delete('/')
@openapi_docs()
@validate()
def delete_all_company_activitys():
    return CompanyActivityService.delete_all()

@company_activity_controller.get('/aggregate')
@openapi_docs()
@validate()
def aggregate_company_activity():
    result = CompanyActivityService.aggregate_company_activity()
    return {"message": result}, 200
