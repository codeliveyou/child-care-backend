from flask import Blueprint, request, jsonify
from src.modules.user.user_service import UserService
from src.modules.user.user_dtos import RegisterUserBody, UpdateUserBody
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from werkzeug.utils import secure_filename

user_controller = Blueprint('users', __name__)

@user_controller.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        body = RegisterUserBody(**data)
        user_id, token = UserService.register(body)
        if not user_id:
            return jsonify({"error": token}), 400

        return jsonify({"_id": user_id, "message": "Registration successful!", "token": token}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@user_controller.route('/change-profile-picture', methods=['PUT'])
@jwt_required()  # Requires user authentication via JWT
def change_profile_picture():
    try:
        # Get the current user's ID from the JWT token
        user_id = get_jwt_identity()

        # Check if the request contains the file
        if 'profile_picture' not in request.files:
            return jsonify({"error": "No profile picture uploaded"}), 400

        # Get the profile picture file
        file = request.files['profile_picture']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Secure the filename
        filename = secure_filename(file.filename)

        # Read the file data
        picture_data = file.read()

        # Call the service to change the profile picture
        success, picture_id = UserService.change_profile_picture(user_id, picture_data, filename)

        if success:
            return jsonify({"message": "Profile picture updated successfully", "picture_id": picture_id}), 200
        else:
            return jsonify({"error": "Failed to update profile picture"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_controller.route('/profile-picture/<picture_id>', methods=['GET'])
def get_profile_picture(picture_id):
    try:
        # Fetch the picture from GridFS
        picture = fs.get(ObjectId(picture_id))
        return send_file(BytesIO(picture.read()), mimetype=picture.content_type)

    except gridfs.errors.NoFile:
        return jsonify({"error": "Profile picture not found"}), 404

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
        # Log or print the specific validation error
        print(f"ValidationError: {e}")
        return jsonify({"error": e.errors()}), 400
    except ValueError as e:
        # Handle ObjectId validation errors here
        return jsonify({"error": str(e)}), 400


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

        token, error = UserService.login(email, password)
        if error:
            return jsonify({"error": error}), 401

        return jsonify({"token": token}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@user_controller.route('/logout/<user_id>', methods=['POST'])
def logout_user(user_id):
    try:
        # Call the service to handle logout
        message = UserService.logout(user_id)
        if "successful" in message:
            return jsonify({"message": message}), 200
        return jsonify({"error": message}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_controller.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = UserService.get_one(user_id)
        if user:
            response = {
                'user_name': user.get('user_name'),
                'user_email': user.get('user_email'),
                'account_description': user.get('account_description')
            }
            return jsonify(response), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500