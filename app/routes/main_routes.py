from flask import Blueprint, jsonify

bp = Blueprint('main_routes', __name__)

@bp.route('/')
def home():
    return jsonify({"message": "Welcome to the Video-to-Video Avatar Interaction Platform!"})
