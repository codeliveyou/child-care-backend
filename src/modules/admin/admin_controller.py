from flask import Blueprint, request, jsonify
from src.modules.admin.admin_service import AdminService
from src.modules.admin.admin_dtos import CreateAdminBody, UpdateAdminBody
from pydantic import ValidationError

admin_controller = Blueprint('admins', __name__)

@admin_controller.route('/', methods=['POST'])
def create_admin():
    try:
        data = request.get_json()
        body = CreateAdminBody(**data)
        admin_id = AdminService.create(body)
        return jsonify({"_id": admin_id}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@admin_controller.route('/', methods=['GET'])
def get_admins():
    admins = AdminService.get_all()
    return jsonify(admins), 200

@admin_controller.route('/<admin_id>', methods=['GET'])
def get_admin(admin_id):
    admin = AdminService.get_one(admin_id)
    if admin:
        return jsonify(admin), 200
    return jsonify({"error": "Admin not found"}), 404

@admin_controller.route('/<admin_id>', methods=['PUT'])
def update_admin(admin_id):
    try:
        data = request.get_json()
        body = UpdateAdminBody(**data)
        updated_admin = AdminService.update_one(admin_id, body)
        if updated_admin:
            return jsonify(updated_admin), 200
        return jsonify({"error": "Admin not found"}), 404
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@admin_controller.route('/<admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    success = AdminService.delete_one(admin_id)
    if success:
        return jsonify({"message": "Admin deleted successfully"}), 200
    return jsonify({"error": "Admin not found"}), 404

@admin_controller.route('/delete-all', methods=['DELETE'])
def delete_all_admins():
    AdminService.delete_all()
    return jsonify({"message": "All admins deleted successfully"}), 200
