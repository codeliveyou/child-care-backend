# import eventlet
# eventlet.monkey_patch()

from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pydantic_docs import OpenAPI
from pymongo import MongoClient
from constants import Constants


from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import uuid
from bson.objectid import ObjectId
import uuid

client = MongoClient(Constants.DATABASE_URL)
db = client["CC-database"]
rooms_collection = db["rooms"]
users_collection = db["users"]
messages_collection = db["messages"]
#
app = Flask(__name__)
app.config["DEBUG"] = False
app.config["CACHE_TYPE"] = "null"
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)


CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}


jwt = JWTManager(app)
# openapi
swagger = OpenAPI(
    endpoint="/docs/swagger/",
    ui="swagger",
    name="swagger",
    extra_props={
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
        "security": [{"bearerAuth": []}],
    },
)
swagger.register(app)
redoc = OpenAPI(endpoint="/docs/redoc/", ui="redoc", name="redoc")
redoc.register(app)
# BP REG
from src.modules.root.root_controller import root_controller

app.register_blueprint(root_controller, url_prefix="/")
from src.modules.user.user_controller import user_controller

app.register_blueprint(user_controller, url_prefix="/users")

from src.modules.admin.admin_controller import admin_controller

app.register_blueprint(admin_controller, url_prefix="/admins")

from src.modules.company.company_controller import company_controller

app.register_blueprint(company_controller, url_prefix="/companys")

from src.modules.invoice.invoice_controller import invoice_controller

app.register_blueprint(invoice_controller, url_prefix="/invoices")

from src.modules.statistics.statistics_controller import statistics_controller

app.register_blueprint(statistics_controller, url_prefix="/statistics")

from src.modules.room.room_controller import room_controller

app.register_blueprint(room_controller, url_prefix="/rooms")

from src.modules.userdata.userdata_controller import userdata_controller

app.register_blueprint(userdata_controller, url_prefix="/userdatas")

from src.modules.user_activity.user_activity_controller import user_activity_controller

app.register_blueprint(user_activity_controller, url_prefix="/user_activitys")


import os
import requests
from flask import request, jsonify
from datetime import datetime

# Metered Secret Key
METERED_SECRET_KEY = os.environ.get("METERED_SECRET_KEY")
# Metered Domain
METERED_DOMAIN = os.environ.get("METERED_DOMAIN")


# API Route to create a meeting room
@app.route("/api/create/room", methods=["POST"])
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
    room_data = r.json()
    room_data["uuid"] = creator_uuid
    room_name = room_data.get("roomName")
    

    # Store the room in MongoDB
    if room_name:
        
        new_room = {
            "room_name": room_name,
            "host": host,
            "created_at": datetime.now(),
            "ended_at": None,
            "participants_count": 1,
            "participants": [
                { "username": host,
                    "role": "creator",
                  "user_id": creator_uuid
                }
            ]
        }
        rooms_collection.insert_one(new_room)
        # return {"success": True, "roomName": room_name}
        print("meeting creation added to db successfully")
    else:
        # return {"success": False, "message": "Room creation failed."}
        print("meeting creation was not added to db")

    return room_data


# API Route to validate meeting
@app.route("/api/validate-meeting")
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


@app.route("/api/room/join")
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
        return {"success": True, "participants_count": room["participants_count"], "uuid": str(user_uuid)}
    return {"success": False, "message": "Room not found."}


@app.route("/api/room/leave")
def leave_room(room_name):
    result = rooms_collection.update_one(
        {"room_name": room_name, "participants_count": {"$gt": 0}},
        {"$inc": {"participants_count": -1}},
    )
    if result.modified_count > 0:
        room = rooms_collection.find_one({"room_name": room_name})
        return {"success": True, "participants_count": room["participants_count"]}
    return {"success": False, "message": "Room not found or no participants."}


@app.route("/api/room/end", methods=["GET"])
def end_meeting():
    room_name = request.args.get("roomName")
    result = rooms_collection.update_one(
        {"room_name": room_name, "ended_at": None},
        {"$set": {"ended_at": datetime.now()}},
    )
    if result.modified_count > 0:
        return {"success": True, "message": "Meeting ended."}
    return {"success": False, "message": "Room not found or already ended."}


@app.route("/api/room/history", methods=["GET"])
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
@app.route("/api/metered-domain")
def get_metered_domain():
    return {"METERED_DOMAIN": METERED_DOMAIN}


@app.route("/")
def index():
    return "Backend"


###################################


@app.route("/http-call")
def http_call():
    """Return JSON with string data as the value"""
    data = {"data": "This text was fetched using an HTTP call to server on render"}
    return jsonify(data)


@socketio.on("init")
def handle_init(data):
    """
    Initialize the connection with user details.
    Expected data: {'username': 'name', 'role': 'role'}
    """
    username = data.get("username")
    role = data.get("role")
    sid = request.sid
    roomName = data.get("roomName")

    user_uuid = str(uuid.uuid4())
    # Update the participants list and increment the count
    if role != 'creator':
        result = rooms_collection.find_one_and_update(
            { "room_name": roomName,
                "participants": {
                    "$not": {
                        "$elemMatch": {
                            "username": username,
                            "role": role
                        }
                    }
                }
            },
            {
                "$addToSet": {
                    "participants": {"username": username, "role": role, "user_id": str(user_uuid)}
                },  # Add user to participants list if not already present
                "$inc": {"participants_count": 1},  # Increment participants count
            },
        )

    room = rooms_collection.find_one({"room_name": roomName})
    # Fetch all users except the current one
    all_users_cursor = room["participants"]
    all_users = [
        {"userid": user["user_id"], "username": user["username"], "role": user["role"]}
        for user in all_users_cursor
    ]

    emit(
        "init_response",
        {"msg": f"Welcome {username}!", "users": all_users},
        broadcast=True,
    )
    print(f"{username} ({role}) connected with SID: {sid}")


@socketio.on("private_message")
def handle_private_message(data):
    """
    Handle private messages between Room Creator and Participants.
    Expected data: {'to': 'recipient_sid', 'message': 'text'}
    """
    from_sid = request.sid
    to_sid = data.get("to")
    message_text = data.get("message")

    sender = users_collection.find_one({"sid": from_sid})
    recipient = users_collection.find_one({"sid": to_sid})

    if sender and recipient:
        # Find or create a private room
        room_id = find_private_room(sender["_id"], recipient["_id"])
        if not room_id:
            room_id = create_room(sender["_id"], recipient["_id"])

        # Join both users to the room
        join_room(room_id, from_sid)
        join_room(room_id, to_sid)

        # Save message to the database
        messages_collection.insert_one(
            {
                "room_id": room_id,
                "sender_id": sender["_id"],
                "message": message_text,
                "timestamp": datetime.datetime.utcnow(),
            }
        )

        # Emit the message to the recipient
        emit(
            "room_message",
            {
                "from": from_sid,
                "message": message_text,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            },
            room=room_id,
        )
        print(f"Private message from {from_sid} to {to_sid}: {message_text}")


def find_private_room(user1_id, user2_id):
    """
    Find a room that includes exactly these two users.
    """
    room = rooms_collection.find_one(
        {"participants": {"$all": [user1_id, user2_id]}, "participants": {"$size": 2}}
    )
    return room["room_id"] if room else None


def create_chat_room(creator_id, participant_id):
    """
    Create a new room for private communication.
    """
    room_id = str(uuid.uuid4())
    rooms_collection.insert_one(
        {
            "room_id": room_id,
            "creator_id": creator_id,
            "participants": [creator_id, participant_id],
            "created_at": datetime.datetime.utcnow(),
        }
    )
    return room_id


users = {}


@socketio.on("connect")
def handle_connect():
    print(f"Client connected: {request.sid}")
    emit("init_response", {"msg": "Connected to server", "users": list(users.values())})


@socketio.on("chat_request")
def handle_chat_request(data):
    """
    Handle chat requests from Guests to Patients.
    Expected data: {'patient_sid': 'patient_socket_id'}
    """
    guest_sid = request.sid
    patient_sid = data.get("patient_sid")

    guest = users_collection.find_one({"sid": guest_sid})
    patient = users_collection.find_one({"sid": patient_sid})

    if guest and patient and patient["role"] == "patient":
        # Notify the Room Creator about the chat request
        creator = users_collection.find_one({"role": "creator"})
        if creator:
            emit(
                "chat_request",
                {
                    "guest_sid": guest_sid,
                    "guest_username": guest["username"],
                    "patient_sid": patient_sid,
                    "patient_username": patient["username"],
                },
                room=creator["sid"],
            )
            print(f"Chat request from {guest_sid} to {patient_sid}")
        else:
            emit("error", {"msg": "Room Creator not connected."}, room=guest_sid)


@socketio.on("chat_response")
def handle_chat_response(data):
    """
    Handle the Room Creator's response to a chat request.
    Expected data: {'guest_sid': 'guest_socket_id', 'patient_sid': 'patient_socket_id', 'approve': True/False}
    """
    guest_sid = data.get("guest_sid")
    patient_sid = data.get("patient_sid")
    approve = data.get("approve")

    guest = users_collection.find_one({"sid": guest_sid})
    patient = users_collection.find_one({"sid": patient_sid})

    if approve:
        # Create a unique room for the Guest and Patient
        room_id = str(uuid.uuid4())
        rooms_collection.insert_one(
            {
                "room_id": room_id,
                "creator_id": guest["_id"],  # Assuming creator manages all rooms
                "participants": [guest["_id"], patient["_id"]],
                "created_at": datetime.datetime.utcnow(),
            }
        )

        # Update users with the room_id
        users_collection.update_one(
            {"_id": guest["_id"]}, {"$set": {"room_id": room_id}}
        )
        users_collection.update_one(
            {"_id": patient["_id"]}, {"$set": {"room_id": room_id}}
        )

        # Join both users to the room
        join_room(room_id, guest_sid)
        join_room(room_id, patient_sid)

        # Notify both users
        emit(
            "chat_approved",
            {"room_id": room_id, "patient_sid": patient_sid, "guest_sid": guest_sid},
            room=guest_sid,
        )

        emit(
            "chat_started",
            {"room_id": room_id, "guest_sid": guest_sid},
            room=patient_sid,
        )

        print(f"Chat approved between {guest_sid} and {patient_sid} in room {room_id}")
    else:
        emit(
            "chat_denied",
            {"msg": "Your chat request was denied by the Room Creator."},
            room=guest_sid,
        )
        print(f"Chat denied for {guest_sid} to chat with {patient_sid}")


@socketio.on("room_message")
def handle_room_message(data):
    """
    Handle messages within a specific room.
    Expected data: {'room_id': 'room_id', 'message': 'text'}
    """
    room_id = data.get("room_id")
    message_text = data.get("message")
    from_name = data.get("from")
    to = data.get("to")
    role = data.get("role")

    sender = users_collection.find_one({"sid": from_name})
    room = rooms_collection.find_one({"room_id": room_id})

    # if sender and room and ObjectId(sender["_id"]) in room["participants"]:
        # Save message to the database
        # messages_collection.insert_one(
        #     {
        #         "room_id": room_id,
        #         "sender_id": sender["_id"],
        #         "message": message_text,
        #         "timestamp": datetime.datetime.utcnow(),
        #     }
        # )

        # Emit the message to the room
    emit(
        "room_message",
        {
            "room": room_id,                
            "from": from_name,
            "to": to,
            "role": role,
            "message": message_text,
            "timestamp": datetime.now().isoformat(),
        },
        # room=room_id,
        broadcast=True
    )
    print(f"Room {room_id}: {from_name} says {message_text} to {to}")


@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    user = users_collection.find_one({"sid": sid})
    if user:
        username = user.get("username", "Unknown")
        role = user.get("role", "Unknown")

        print(f"{username} ({role}) disconnected.")

        # Notify others about the disconnection
        emit("user_disconnected", {"sid": sid, "username": username}, broadcast=True)

        # Leave any rooms the user was part of
        room_id = user.get("room_id")
        if room_id:
            leave_room(room_id, sid)

        # Remove from connected users
        users_collection.delete_one({"_id": user["_id"]})


@socketio.on("get_chat_history")
def handle_get_chat_history(data):
    """
    Retrieve chat history for a specific room.
    Expected data: {'room_id': 'room_id'}
    """
    room_id = data.get("room_id")
    messages_cursor = messages_collection.find({"room_id": room_id}).sort(
        "timestamp", 1
    )
    messages = [
        {
            "sender_id": str(msg["sender_id"]),
            "message": msg["message"],
            "timestamp": msg["timestamp"].isoformat(),
        }
        for msg in messages_cursor
    ]
    emit("chat_history", {"room_id": room_id, "messages": messages})


def get_creator_sid():
    """Return the SID of the Room Creator."""
    creator = users_collection.find_one({"role": "creator"})
    return creator["sid"] if creator else None
