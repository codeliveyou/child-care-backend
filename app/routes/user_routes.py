from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo
from werkzeug.security import generate_password_hash

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = {
        "username": data['username'],
        "email": data['email'],
        "password_hash": generate_password_hash(data['password']),
        "company_id": ObjectId(data['company_id']),
        "role": data['role'],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = mongo.db.users.insert_one(user)
    return jsonify({"_id": str(result.inserted_id)}), 201

@user_blueprint.route('/', methods=['GET'])
def get_users():
    users = list(mongo.db.users.find())
    for user in users:
        user['_id'] = str(user['_id'])
        user['company_id'] = str(user['company_id'])
    return jsonify(users), 200

@user_blueprint.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        user['company_id'] = str(user['company_id'])
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    update_data = {
        "username": data.get('username'),
        "email": data.get('email'),
        "role": data.get('role'),
        "updated_at": datetime.utcnow()
    }
    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return jsonify({"message": "User updated successfully"}), 200

@user_blueprint.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "User deleted successfully"}), 200
