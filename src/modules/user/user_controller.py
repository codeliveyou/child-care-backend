from flask import Blueprint, request, jsonify
from src.modules.user.user_service import UserService
from src.modules.user.user_dtos import RegisterUserBody
from pydantic import ValidationError

user_controller = Blueprint('users', __name__)

@user_controller.route('/register', methods=['POST'])
def register_user():
    try:
        # Parse and validate the input data
        data = request.get_json()
        body = RegisterUserBody(**data)

        # Register the user
        user_id, error = UserService.register(body)
        if error:
            return jsonify({"error": error}), 400

        return jsonify({"_id": user_id, "message": "Registration successful!"}), 201

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@user_controller.route('/', methods=['GET'])
def get_users():
    users = UserService.get_all()
    return jsonify(users), 200

@user_controller.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_one(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@user_controller.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        body = UpdateUserBody(**data)
        updated_user = UserService.update_one(user_id, body)
        if updated_user:
            updated_user['_id'] = str(updated_user['_id'])
            return jsonify(updated_user), 200
        return jsonify({"error": "User not found"}), 404
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@user_controller.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserService.delete_one(user_id)
    if success:
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@user_controller.route('/delete-all', methods=['DELETE'])
def delete_all_users():
    UserService.delete_all()
    return jsonify({"message": "All users deleted successfully"}), 200


@user_controller.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Call the service to handle login
        token, error = UserService.login(email, password)
        if error:
            return jsonify({"error": error}), 401

        return jsonify({"token": token}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400