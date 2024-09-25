from flask import Blueprint
from flask_pydantic import validate
from src.modules.user_activity.user_activity_service import User_activityService
from src.modules.user_activity.user_activity_dtos import CreateUser_activityBody, UpdateUser_activityBody
from src.utils.responder import Responder
from flask_pydantic_docs import openapi_docs

user_activity_controller = Blueprint('user_activitys', __name__)


@user_activity_controller.post('/')
@openapi_docs()
@validate()
def create_user_activity(body: CreateUser_activityBody):
    return User_activityService.create(body)

@user_activity_controller.get('/<id>')
@openapi_docs()
@validate()
def get_one_user_activity(id):
    return User_activityService.get_one(id)

@user_activity_controller.get('/')
@openapi_docs()
@validate()
def get_all_user_activitys():
    return User_activityService.get_all()

@user_activity_controller.put('/<id>')
@openapi_docs()
@validate()
def update_one_user_activity(id, body: UpdateUser_activityBody):
    return User_activityService.update_one(id, body)

@user_activity_controller.delete('/<id>')
@openapi_docs()
@validate()
def delete_one_user_activity(id):
    return User_activityService.delete_one(id)

@user_activity_controller.delete('/')
@openapi_docs()
@validate()
def delete_all_user_activitys():
    return User_activityService.delete_all()

