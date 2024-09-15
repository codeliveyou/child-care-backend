from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from src.modules.system_usage.system_usage_service import SystemUsageService
from src.modules.system_usage.system_usage_dtos import CreateSystemUsageBody, UpdateSystemUsageBody

system_usage_controller = Blueprint('system_usages', __name__)

@system_usage_controller.post('/')
@validate()
def create_system_usage(body: CreateSystemUsageBody):
    usage_id = SystemUsageService.create(body)
    return jsonify({"_id": usage_id, "message": "System usage created successfully"}), 201

@system_usage_controller.get('/<id>')
@validate()
def get_one_system_usage(id: str):
    usage = SystemUsageService.get_one(id)
    if usage:
        return jsonify(usage), 200
    return jsonify({"error": "System usage not found"}), 404

@system_usage_controller.get('/')
@validate()
def get_all_system_usages():
    usages = SystemUsageService.get_all()
    return jsonify(usages), 200

@system_usage_controller.put('/<id>')
@validate()
def update_one_system_usage(id: str, body: UpdateSystemUsageBody):
    updated_usage = SystemUsageService.update_one(id, body)
    if updated_usage:
        return jsonify(updated_usage), 200
    return jsonify({"error": "System usage not found"}), 404

@system_usage_controller.delete('/<id>')
@validate()
def delete_one_system_usage(id: str):
    success = SystemUsageService.delete_one(id)
    if success:
        return jsonify({"message": "System usage deleted successfully"}), 200
    return jsonify({"error": "System usage not found"}), 404

@system_usage_controller.delete('/')
@validate()
def delete_all_system_usages():
    SystemUsageService.delete_all()
    return jsonify({"message": "All system usages deleted successfully"}), 200