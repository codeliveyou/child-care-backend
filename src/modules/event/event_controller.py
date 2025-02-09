from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.modules.event.event_service import EventService
from src.modules.event.event_dtos import CreateEventBody, UpdateEventBody
from src.utils.responder import Responder
from flask_openapi3 import Tag
from datetime import datetime

event_tag = Tag(name="events", description="Event management operations")
event_controller = Blueprint('events', __name__)

@event_controller.post('/')
@jwt_required()
def create_event():
    body = request.get_json()
    event_id = EventService.create(body)
    return jsonify({"message": "Event created successfully", "event_id": event_id}), 201

@event_controller.get('/<event_id>')
@jwt_required()
def get_one_event(event_id):
    event = EventService.get_one(event_id)
    if event:
        return jsonify(event), 200
    return jsonify({"error": "Event not found"}), 404

@event_controller.get('/')
@jwt_required()
def get_all_events():
    user_id = get_jwt_identity()
    events = EventService.get_all(user_id)
    return jsonify(events), 200

@event_controller.route('/user-events', methods=['GET'])
@jwt_required()
def get_user_events():
    try:
        user_id = get_jwt_identity()
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Please provide both start_date and end_date"}), 400

        events = EventService.get_user_events(user_id, start_date, end_date)
        return jsonify(events), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@event_controller.put('/<event_id>')
@jwt_required()
def update_one_event(event_id):
    body = request.get_json()
    success = EventService.update_one(event_id, body)
    if success:
        return jsonify({"message": "Event updated successfully"}), 200
    return jsonify({"error": "Event not found or update failed"}), 404

@event_controller.delete('/<event_id>')
@jwt_required()
def delete_one_event(event_id):
    success = EventService.delete_one(event_id)
    if success:
        return jsonify({"message": "Event deleted successfully"}), 200
    return jsonify({"error": "Event not found"}), 404

@event_controller.delete('/')
@jwt_required()
def delete_all_events():
    user_id = get_jwt_identity()
    deleted_count = EventService.delete_all(user_id)
    return jsonify({"message": f"{deleted_count} events deleted successfully"}), 200