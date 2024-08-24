from flask import Blueprint, request, jsonify
from src.modules.room.room_service import RoomService
from src.modules.room.room_dtos import CreateRoomBody, UpdateRoomBody
from pydantic import ValidationError

room_controller = Blueprint('rooms', __name__)

@room_controller.route('/', methods=['POST'])
def create_room():
    try:
        data = request.get_json()
        body = CreateRoomBody(**data)
        room_id = RoomService.create(body)
        if room_id:
            return jsonify({"_id": room_id}), 201
        return jsonify({"error": "Failed to create room"}), 500
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        print(f"Error in create_room: {e}")
        return jsonify({"error": str(e)}), 500

@room_controller.route('/', methods=['GET'])
def get_rooms():
    try:
        rooms = RoomService.get_all()
        return jsonify(rooms), 200
    except Exception as e:
        print(f"Error in get_rooms: {e}")
        return jsonify({"error": str(e)}), 500

@room_controller.route('/<room_id>', methods=['GET'])
def get_room(room_id):
    try:
        room = RoomService.get_one(room_id)
        if room:
            return jsonify(room), 200
        return jsonify({"error": "Room not found"}), 404
    except Exception as e:
        print(f"Error in get_room: {e}")
        return jsonify({"error": str(e)}), 500

@room_controller.route('/<room_id>', methods=['PUT'])
def update_room(room_id):
    try:
        data = request.get_json()
        body = UpdateRoomBody(**data)
        updated_room = RoomService.update_one(room_id, body)
        if updated_room:
            return jsonify(updated_room), 200
        return jsonify({"error": "Room not found"}), 404
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        print(f"Error in update_room: {e}")
        return jsonify({"error": str(e)}), 500

@room_controller.route('/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    try:
        success = RoomService.delete_one(room_id)
        if success:
            return jsonify({"message": "Room deleted successfully"}), 200
        return jsonify({"error": "Room not found"}), 404
    except Exception as e:
        print(f"Error in delete_room: {e}")
        return jsonify({"error": str(e)}), 500

@room_controller.route('/delete-all', methods=['DELETE'])
def delete_all_rooms():
    try:
        RoomService.delete_all()
        return jsonify({"message": "All rooms deleted successfully"}), 200
    except Exception as e:
        print(f"Error in delete_all_rooms: {e}")
        return jsonify({"error": str(e)}), 500
