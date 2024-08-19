from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from main import mongo
from werkzeug.security import generate_password_hash

admin_blueprint = Blueprint('admin_blueprint', __name__)

@admin_blueprint.route('/', methods=['POST'])
def create_admin():
    data = request.get_json()
    admin = {
        "admin_name": data['admin_name'],
        "email": data['email'],
        "password_hash": generate_password_hash(data['password']),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = mongo.db.admins.insert_one(admin)
    return jsonify({"_id": str(result.inserted_id)}), 201

@admin_blueprint.route('/', methods=['GET'])
def get_admins():
    admins = list(mongo.db.admins.find())
    for admin in admins:
        admin['_id'] = str(admin['_id'])
    return jsonify(admins), 200

@admin_blueprint.route('/<admin_id>', methods=['GET'])
def get_admin(admin_id):
    admin = mongo.db.admins.find_one({"_id": ObjectId(admin_id)})
    if admin:
        admin['_id'] = str(admin['_id'])
        return jsonify(admin), 200
    return jsonify({"error": "Admin not found"}), 404

@admin_blueprint.route('/<admin_id>', methods=['PUT'])
def update_admin(admin_id):
    data = request.get_json()
    update_data = {
        "admin_name": data.get('admin_name'),
        "email": data.get('email'),
        "updated_at": datetime.utcnow()
    }
    mongo.db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": update_data})
    return jsonify({"message": "Admin updated successfully"}), 200

@admin_blueprint.route('/<admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    mongo.db.admins.delete_one({"_id": ObjectId(admin_id)})
    return jsonify({"message": "Admin deleted successfully"}), 200
