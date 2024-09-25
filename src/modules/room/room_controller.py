from flask import Blueprint, request, jsonify
from src.modules.room.room_service import RoomService
from src.modules.room.room_dtos import CreateRoomBody, UpdateRoomBody
from pydantic import ValidationError
from datetime import datetime

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
    
@room_controller.route('/fetch_rooms_data', methods=['GET'])
def fetch_rooms_data():

    def format_created_at(created_at):
        current_time = datetime.now()

        if created_at.date() == current_time.date():
            return created_at.strftime('%H:%M')
        else:
            return created_at.strftime('%d:%H:%M')

    def serialzie_room(room):
        return {
        '_id': str(room['_id']),
        'room_name': room['room_name'],
        'host': room['host'],
        'created_at': format_created_at(room['created_at']) if isinstance(room['created_at'], datetime) else None,
        'ended_at': room['ended_at'].isoformat() if isinstance(room['ended_at'], datetime) else None,
        'participants_count': room['participants_count']
    }

    try:
        rooms = RoomService.get_all()
        serialzied_rooms = [serialzie_room(room) for room in rooms]
        return jsonify(serialzied_rooms), 200
    except Exception as e:
        print(f"Error in fetching rooms data: {e}")
        return jsonify({"error": str(e)}), 500
    
@room_controller.route('/fetch_room_data', methods=['POST'])
def fetch_room_data():

    try:
        data = request.get_json()
        print('data',data)
        room = RoomService.get_one(data['roomName'])
        return jsonify({"data": room}), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        print(f"Error in create_room: {e}")
        return jsonify({"error": str(e)}), 500
