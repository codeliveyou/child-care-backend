from flask import Blueprint
from flask_pydantic import validate
from src.modules.admin.admin_service import AdminService
from src.modules.admin.admin_dtos import CreateAdminBody, UpdateAdminBody
from src.utils.responder import Responder
from flask_pydantic_docs import openapi_docs

admin_controller = Blueprint('admins', __name__)


@admin_controller.post('/')
@openapi_docs()
@validate()
def create_admin(body: CreateAdminBody):
    return AdminService.create(body)

@admin_controller.get('/<id>')
@openapi_docs()
@validate()
def get_one_admin(id):
    return AdminService.get_one(id)

@admin_controller.get('/')
@openapi_docs()
@validate()
def get_all_admins():
    return AdminService.get_all()

@admin_controller.put('/<id>')
@openapi_docs()
@validate()
def update_one_admin(id, body: UpdateAdminBody):
    return AdminService.update_one(id, body)

@admin_controller.delete('/<id>')
@openapi_docs()
@validate()
def delete_one_admin(id):
    return AdminService.delete_one(id)

@admin_controller.delete('/')
@openapi_docs()
@validate()
def delete_all_admins():
    return AdminService.delete_all()

