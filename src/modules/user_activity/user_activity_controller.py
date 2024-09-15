from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from src.modules.user_activity.user_activity_service import UserActivityService
from src.modules.user_activity.user_activity_dtos import CreateUserActivityBody, UpdateUserActivityBody

user_activity_controller = Blueprint('user_activitys', __name__)

@user_activity_controller.post('/')
@validate()
def create_user_activity(body: CreateUserActivityBody):
    activity_id = UserActivityService.create(body)
    return jsonify({"_id": activity_id, "message": "User activity created successfully"}), 201

@user_activity_controller.get('/<id>')
@validate()
def get_one_user_activity(id):
    activity = UserActivityService.get_one(id)
    if activity:
        return jsonify(activity), 200
    return jsonify({"error": "User activity not found"}), 404

@user_activity_controller.get('/')
@validate()
def get_all_user_activities():
    activities = UserActivityService.get_all()
    return jsonify(activities), 200

@user_activity_controller.put('/<id>')
@validate()
def update_one_user_activity(id, body: UpdateUserActivityBody):
    updated_activity = UserActivityService.update_one(id, body)
    if updated_activity:
        return jsonify(updated_activity), 200
    return jsonify({"error": "User activity not found"}), 404

@user_activity_controller.delete('/<id>')
@validate()
def delete_one_user_activity(id):
    success = UserActivityService.delete_one(id)
    if success:
        return jsonify({"message": "User activity deleted successfully"}), 200
    return jsonify({"error": "User activity not found"}), 404

@user_activity_controller.delete('/')
@validate()
def delete_all_user_activities():
    UserActivityService.delete_all()
    return jsonify({"message": "All user activities deleted successfully"}), 200
