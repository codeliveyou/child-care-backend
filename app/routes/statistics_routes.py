from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo

statistics_blueprint = Blueprint('statistics_blueprint', __name__)

@statistics_blueprint.route('/', methods=['POST'])
def create_statistics():
    data = request.get_json()
    statistics = {
        "company_id": ObjectId(data['company_id']),
        "user_id": ObjectId(data['user_id']) if data.get('user_id') else None,
        "time_spent": data['time_spent'],
        "sessions_count": data['sessions_count'],
        "rooms_count": data['rooms_count'],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = mongo.db.statistics.insert_one(statistics)
    return jsonify({"_id": str(result.inserted_id)}), 201

@statistics_blueprint.route('/', methods=['GET'])
def get_statistics():
    statistics = list(mongo.db.statistics.find())
    for stat in statistics:
        stat['_id'] = str(stat['_id'])
        stat['company_id'] = str(stat['company_id'])
        if stat.get('user_id'):
            stat['user_id'] = str(stat['user_id'])
    return jsonify(statistics), 200

@statistics_blueprint.route('/<stat_id>', methods=['GET'])
def get_statistics_by_id(stat_id):
    stat = mongo.db.statistics.find_one({"_id": ObjectId(stat_id)})
    if stat:
        stat['_id'] = str(stat['_id'])
        stat['company_id'] = str(stat['company_id'])
        if stat.get('user_id'):
            stat['user_id'] = str(stat['user_id'])
        return jsonify(stat), 200
    return jsonify({"error": "Statistics not found"}), 404

@statistics_blueprint.route('/<stat_id>', methods=['PUT'])
def update_statistics(stat_id):
    data = request.get_json()
    update_data = {
        "time_spent": data.get('time_spent'),
        "sessions_count": data.get('sessions_count'),
        "rooms_count": data.get('rooms_count'),
        "updated_at": datetime.utcnow()
    }
    mongo.db.statistics.update_one({"_id": ObjectId(stat_id)}, {"$set": update_data})
    return jsonify({"message": "Statistics updated successfully"}), 200

@statistics_blueprint.route('/<stat_id>', methods=['DELETE'])
def delete_statistics(stat_id):
    mongo.db.statistics.delete_one({"_id": ObjectId(stat_id)})
    return jsonify({"message": "Statistics deleted successfully"}), 200
