from flask import Blueprint, request, jsonify
from src.modules.userdata.userdata_service import UserDataService
from src.modules.userdata.userdata_dtos import CreateUserDataBody, UpdateUserDataBody
from pydantic import ValidationError

userdata_controller = Blueprint('userdatas', __name__)

@userdata_controller.route('/', methods=['POST'])
def create_userdata():
    try:
        data = request.get_json()
        body = CreateUserDataBody(**data)
        userdata_id = UserDataService.create(body)
        if userdata_id:
            return jsonify({"_id": userdata_id}), 201
        return jsonify({"error": "Failed to create userdata"}), 500
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        print(f"Error in create_userdata: {e}")
        return jsonify({"error": str(e)}), 500

@userdata_controller.route('/', methods=['GET'])
def get_userdata():
    try:
        userdata_list = UserDataService.get_all()
        return jsonify(userdata_list), 200
    except Exception as e:
        print(f"Error in get_userdata: {e}")
        return jsonify({"error": str(e)}), 500

@userdata_controller.route('/<userdata_id>', methods=['GET'])
def get_userdata_by_id(userdata_id):
    try:
        userdata = UserDataService.get_one(userdata_id)
        if userdata:
            return jsonify(userdata), 200
        return jsonify({"error": "Userdata not found"}), 404
    except Exception as e:
        print(f"Error in get_userdata_by_id: {e}")
        return jsonify({"error": str(e)}), 500

@userdata_controller.route('/<userdata_id>', methods=['PUT'])
def update_userdata(userdata_id):
    try:
        data = request.get_json()
        body = UpdateUserDataBody(**data)
        updated_userdata = UserDataService.update_one(userdata_id, body)
        if updated_userdata:
            return jsonify(updated_userdata), 200
        return jsonify({"error": "Userdata not found"}), 404
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        print(f"Error in update_userdata: {e}")
        return jsonify({"error": str(e)}), 500

@userdata_controller.route('/<userdata_id>', methods=['DELETE'])
def delete_userdata(userdata_id):
    try:
        success = UserDataService.delete_one(userdata_id)
        if success:
            return jsonify({"message": "Userdata deleted successfully"}), 200
        return jsonify({"error": "Userdata not found"}), 404
    except Exception as e:
        print(f"Error in delete_userdata: {e}")
        return jsonify({"error": str(e)}), 500

@userdata_controller.route('/delete-all', methods=['DELETE'])
def delete_all_userdata():
    try:
        UserDataService.delete_all()
        return jsonify({"message": "All userdata deleted successfully"}), 200
    except Exception as e:
        print(f"Error in delete_all_userdata: {e}")
        return jsonify({"error": str(e)}), 500
