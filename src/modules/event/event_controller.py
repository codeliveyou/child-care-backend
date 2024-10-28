from flask import Blueprint, jsonify, request
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.modules.event.event_service import EventService
from src.modules.event.event_dtos import CreateEventBody, UpdateEventBody
from src.utils.responder import Responder
from flask_pydantic_docs import openapi_docs
from datetime import datetime

event_controller = Blueprint('events', __name__)

@event_controller.post('/')
@jwt_required()
@openapi_docs()
@validate()
def create_event(body: CreateEventBody):
    event_id = EventService.create(body)
    return jsonify({"message": "Event created successfully", "event_id": event_id}), 201

@event_controller.get('/<event_id>')
@jwt_required()
@openapi_docs()
@validate()
def get_one_event(event_id):
    event = EventService.get_one(event_id)
    if event:
        return jsonify(event), 200
    return jsonify({"error": "Event not found"}), 404

@event_controller.get('/')
@jwt_required()
@openapi_docs()
def get_all_events():
    user_id = get_jwt_identity()
    events = EventService.get_all(user_id)
    return jsonify(events), 200

@event_controller.route('/user-events', methods=['GET'])
@jwt_required()  # Requires authentication
def get_user_events():
    try:
        # Get the current user's ID from the JWT token
        user_id = get_jwt_identity()

        # Get date range from query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Validate that both dates are provided
        if not start_date or not end_date:
            return jsonify({"error": "Please provide both start_date and end_date"}), 400

        # Fetch events within the date range
        events = EventService.get_user_events(user_id, start_date, end_date)
        return jsonify(events), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@event_controller.put('/<event_id>')
@jwt_required()
@openapi_docs()
@validate()
def update_one_event(event_id, body: UpdateEventBody):
    success = EventService.update_one(event_id, body)
    if success:
        return jsonify({"message": "Event updated successfully"}), 200
    return jsonify({"error": "Event not found or update failed"}), 404

@event_controller.delete('/<event_id>')
@jwt_required()
@openapi_docs()
def delete_one_event(event_id):
    success = EventService.delete_one(event_id)
    if success:
        return jsonify({"message": "Event deleted successfully"}), 200
    return jsonify({"error": "Event not found"}), 404

@event_controller.delete('/')
@jwt_required()
@openapi_docs()
def delete_all_events():
    user_id = get_jwt_identity()
    deleted_count = EventService.delete_all(user_id)
    return jsonify({"message": f"{deleted_count} events deleted successfully"}), 200
