from flask import Blueprint, request, jsonify
from src.modules.admin.admin_service import AdminService
from src.modules.admin.admin_dtos import CreateAdminBody, UpdateAdminBody
from pydantic import ValidationError
from src.modules.user.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity


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

@admin_controller.route('/login', methods=['POST'])
def login_admin():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate email and password
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Call the AdminService to handle the login
        token, error = AdminService.login(email, password)
        if error:
            return jsonify({"error": error}), 401

        return jsonify({"token": token}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    

@admin_controller.route('/users', methods=['GET'])
def get_users():
    # Extract pagination parameters (default: page 1, page size 10)
    try:
        page = int(request.args.get('page', 1))  # Default to page 1
        page_size = int(request.args.get('page_size', 10))  # Default to page size 10

        # Fetch paginated users from UserService
        result = UserService.get_all(page=page, page_size=page_size)
        
        return jsonify(result), 200
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

@admin_controller.route('/me', methods=['GET'])
@jwt_required()  # Enforce JWT authentication
def get_current_admin():
    try:
        # Extract the admin_id from the JWT token
        admin_id = get_jwt_identity()

        # Fetch the admin details from the database
        admin = AdminService.get_one(admin_id)
        if admin:
            # Prepare the response with the necessary fields
            response = {
                'email': admin.get('email')
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "Admin not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
