from flask import Blueprint, request, jsonify
from src.modules.room.room_service import RoomService
from src.modules.room.room_dtos import CreateRoomBody, UpdateRoomBody
from pydantic import ValidationError
from datetime import datetime
import os
import requests
import uuid
from pymongo import MongoClient
from constants import Constants

room_controller = Blueprint("rooms", __name__)

client = MongoClient(Constants.DATABASE_URL)
db = client["CC-database"]
rooms_collection = db["rooms"]
meetings_collection = db["meetings"]


# @room_controller.route('/', methods=['POST'])
# def create_room():
#     try:
#         data = request.get_json()
#         body = CreateRoomBody(**data)
#         room_id = RoomService.create(body)
#         if room_id:
#             return jsonify({"_id": room_id}), 201
#         return jsonify({"error": "Failed to create room"}), 500
#     except ValidationError as e:
#         return jsonify({"error": e.errors()}), 400
#     except Exception as e:
#         print(f"Error in create_room: {e}")
#         return jsonify({"error": str(e)}), 500

# @room_controller.route('/', methods=['GET'])
# def get_rooms():
#     try:
#         rooms = RoomService.get_all()
#         return jsonify(rooms), 200
#     except Exception as e:
#         print(f"Error in get_rooms: {e}")
#         return jsonify({"error": str(e)}), 500

# @room_controller.route('/<room_id>', methods=['GET'])
# def get_room(room_id):
#     try:
#         room = RoomService.get_one(room_id)
#         if room:
#             return jsonify(room), 200
#         return jsonify({"error": "Room not found"}), 404
#     except Exception as e:
#         print(f"Error in get_room: {e}")
#         return jsonify({"error": str(e)}), 500

# @room_controller.route('/<room_id>', methods=['PUT'])
# def update_room(room_id):
#     try:
#         data = request.get_json()
#         body = UpdateRoomBody(**data)
#         updated_room = RoomService.update_one(room_id, body)
#         if updated_room:
#             return jsonify(updated_room), 200
#         return jsonify({"error": "Room not found"}), 404
#     except ValidationError as e:
#         return jsonify({"error": e.errors()}), 400
#     except Exception as e:
#         print(f"Error in update_room: {e}")
#         return jsonify({"error": str(e)}), 500

# @room_controller.route('/<room_id>', methods=['DELETE'])
# def delete_room(room_id):
#     try:
#         success = RoomService.delete_one(room_id)
#         if success:
#             return jsonify({"message": "Room deleted successfully"}), 200
#         return jsonify({"error": "Room not found"}), 404
#     except Exception as e:
#         print(f"Error in delete_room: {e}")
#         return jsonify({"error": str(e)}), 500

# @room_controller.route('/delete-all', methods=['DELETE'])
# def delete_all_rooms():
#     try:
#         RoomService.delete_all()
#         return jsonify({"message": "All rooms deleted successfully"}), 200
#     except Exception as e:
#         print(f"Error in delete_all_rooms: {e}")
#         return jsonify({"error": str(e)}), 500


@room_controller.route("/fetch_rooms_data", methods=["POST"])
def fetch_rooms_data():

    def format_created_at(created_at):
        current_time = datetime.now()

        if created_at.date() == current_time.date():
            return created_at.strftime("%H:%M")
        else:
            return created_at.strftime("%d:%H:%M")

    def serialzie_room(room):
        return {
            "_id": str(room["_id"]),
            "room_name": room["room_name"],
            "host": room["host"],
            "created_at": (
                format_created_at(room["created_at"])
                if isinstance(room["created_at"], datetime)
                else None
            ),
            "ended_at": (
                room["ended_at"].isoformat()
                if isinstance(room["ended_at"], datetime)
                else None
            ),
            "participants_count": room["participants_count"],
            "avatar_type": room["avatar_type"],
            "patient_name": room["patient_name"],
        }

    try:
        data = request.get_json()
        rooms = RoomService.get_all(data["userEmail"])
        serialzied_rooms = [serialzie_room(room) for room in rooms]
        return jsonify(serialzied_rooms), 200
    except Exception as e:
        print(f"Error in fetching rooms data: {e}")
        return jsonify({"error": str(e)}), 500


@room_controller.route("/fetch_room_data", methods=["POST"])
def fetch_room_data():

    try:
        data = request.get_json()
        print("data", data)
        room = RoomService.get_one(data["roomName"])
        return jsonify({"data": room}), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        print(f"Error in create_room: {e}")
        return jsonify({"error": str(e)}), 500


# Metered Secret Key
METERED_SECRET_KEY = os.environ.get("METERED_SECRET_KEY")
# Metered Domain
METERED_DOMAIN = os.environ.get("METERED_DOMAIN")


# API Route to create a meeting room
@room_controller.route("/create", methods=["POST"])
def create_room():

    creator_uuid = str(uuid.uuid4())

    r = requests.post(
        "https://"
        + METERED_DOMAIN
        + "/api/v1/room"
        + "?secretKey="
        + METERED_SECRET_KEY
    )

    data = request.get_json()

    host = data.get("username", "Unknown Host")
    email = data.get("userEmail", "Unknown Email")
    room_data = r.json()
    room_data["uuid"] = creator_uuid
    room_name = room_data.get("roomName")
    print("room_data", room_data)
    patient_name = data.get("patientName")
    patient_personal_id = data.get("patientPersonalID")
    avatar_type = data.get("avatarType")
    voice_type = data.get("voiceType")
    avatar_name = data.get("avatarName")
    patient_password = data.get("p_pass")
    guest_password = data.get("g_pass")
    # Store the room in MongoDB
    if room_name:

        new_room = {
            "host": host,
            "email": email,
            "room_name": room_name,
            "patient_name": patient_name,
            "patient_personal_id": patient_personal_id,
            "patient_password": patient_password,
            "guest_password": guest_password,
            "avatar_type": avatar_type,
            "voice_type": voice_type,
            "avatar_name": avatar_name,
            "created_at": datetime.now(),
            "ended_at": None,
            "participants_count": 1,
            "participants": [
                {"username": host, "role": "creator", "user_id": creator_uuid}
            ],
        }
        rooms_collection.insert_one(new_room)
        # return {"success": True, "roomName": room_name}
        print("meeting creation added to db successfully")
    else:
        # return {"success": False, "message": "Room creation failed."}
        print("meeting creation was not added to db")

    return room_data


# API Route to validate meeting
@room_controller.route("/validate-meeting", methods=["GET"])
def validate_meeting():
    roomName = request.args.get("roomName")
    if roomName:
        r = requests.get(
            "https://"
            + METERED_DOMAIN
            + "/api/v1/room/"
            + roomName
            + "?secretKey="
            + METERED_SECRET_KEY
        )
        data = r.json()
        if data.get("roomName"):
            return {"roomFound": True}
        else:
            return {"roomFound": False}
    else:
        return {"success": False, "message": "Please specify roomName"}


@room_controller.route("/join")
def join_room():
    room_name = request.args.get("roomName")
    username = request.args.get("userName")
    user_role = request.args.get("role")

    if not room_name or not username:
        return {"success": False, "message": "Room name and username are required."}

    room = rooms_collection.find_one({"room_name": room_name})
    if not room:
        return {"success": False, "message": "Room not found."}

    # Check if the user is already in the participants list
    if username in room.get("participants", []):
        return {"success": False, "message": "User already in the room."}

    user_uuid = str(uuid.uuid4())
    # Update the participants list and increment the count
    # result = rooms_collection.update_one(
    #     {"room_name": room_name},
    #     {
    #         "$addToSet": {
    #             "participants": {"username": username, "role": user_role, "user_id": str(user_uuid)}
    #         },  # Add user to participants list if not already present
    #         "$inc": {"participants_count": 1},  # Increment participants count
    #     },
    # )

    # if result.modified_count > 0:
    if True:
        room = rooms_collection.find_one({"room_name": room_name})
        return {
            "success": True,
            "participants_count": room["participants_count"],
            "uuid": str(user_uuid),
        }
    return {"success": False, "message": "Room not found."}


@room_controller.route("/leave", methods=["GET"])
def leave_room():
    try:
        room_name = request.args.get("roomName")
        print("found room", room_name)
        username = request.args.get("userName")
        role = request.args.get("role")

        print("username", username)
        if not room_name or not username or not role:
            print(1)
            return {
                "success": False,
                "message": "Room name, username, and role are required.",
            }

        result = rooms_collection.update_one(
            {"room_name": room_name},
            {
                "$pull": {"participants": {"username": username, "role": role}},
                "$inc": {"participants_count": -1},
            },
        )
        print(2)

        if result.modified_count > 0:
            print(3)
            room = rooms_collection.find_one({"room_name": room_name})
            return {"success": True, "participants_count": room["participants_count"]}
        return {
            "success": False,
            "message": "User not found in the room or room doesn't exist.",
        }
    except Exception as e:
        print("Error: ", e)
        return {"success": False, "message": str(e)}


@room_controller.route("/end", methods=["GET"])
def end_meeting():
    room_name = request.args.get("roomName")
    result = rooms_collection.update_one(
        {"room_name": room_name, "ended_at": None},
        {"$set": {"ended_at": datetime.now()}},
    )
    if result.modified_count > 0:
        return {"success": True, "message": "Meeting ended."}
    return {"success": False, "message": "Room not found or already ended."}


@room_controller.route("/history", methods=["GET"])
def get_room_history():
    room_name = request.args.get("roomName")
    room = meetings_collection.find_one({"room_name": room_name})

    if room:
        history = {
            "room_name": room["room_name"],
            "host": room["host"],
            "created_at": room["created_at"],
            "ended_at": room["ended_at"],
            "participants_count": room["participants_count"],
        }
        return {"success": True, "room_history": history}

    return {"success": False, "message": "Room not found."}


# API Route to fetch the Metered Domain
@room_controller.route("/metered-domain", methods=["GET"])
def get_metered_domain():
    return {"METERED_DOMAIN": METERED_DOMAIN}


@room_controller.route("/check_patient_authentication", methods=["POST"])
def check_patient_authentication():
    data = request.get_json()
    room_id = data.get("roomName")
    patient_password = data.get("patientPassword")
    rlt = RoomService.check_patient_authentication(room_id, patient_password)
    if rlt == True:
        return {"message": "ok"}

    return {"message": "no"}


@room_controller.route("/check_guest_authentication", methods=["POST"])
def check_guest_authentication():
    data = request.get_json()
    room_id = data.get("roomName")
    guest_password = data.get("guestPassword")
    rlt = RoomService.check_guest_authentication(room_id, guest_password)
    if rlt == True:
        return {"message": "ok"}
    return {"message": "no"}
