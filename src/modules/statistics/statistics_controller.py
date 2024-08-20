from flask import Blueprint, request, jsonify
from src.modules.statistics.statistics_service import StatisticsService
from src.modules.statistics.statistics_dtos import CreateStatisticsBody, UpdateStatisticsBody
from pydantic import ValidationError

statistics_controller = Blueprint('statistics', __name__)

@statistics_controller.route('/', methods=['POST'])
def create_statistics():
    try:
        data = request.get_json()
        body = CreateStatisticsBody(**data)
        stat_id = StatisticsService.create(body)
        return jsonify({"_id": stat_id}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@statistics_controller.route('/', methods=['GET'])
def get_statistics():
    stats = StatisticsService.get_all()
    return jsonify(stats), 200

@statistics_controller.route('/<stat_id>', methods=['GET'])
def get_statistics_by_id(stat_id):
    stat = StatisticsService.get_one(stat_id)
    if stat:
        return jsonify(stat), 200
    return jsonify({"error": "Statistics record not found"}), 404

@statistics_controller.route('/<stat_id>', methods=['PUT'])
def update_statistics(stat_id):
    try:
        data = request.get_json()
        body = UpdateStatisticsBody(**data)
        updated_stat = StatisticsService.update_one(stat_id, body)
        if updated_stat:
            return jsonify(updated_stat), 200
        return jsonify({"error": "Statistics record not found"}), 404
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@statistics_controller.route('/<stat_id>', methods=['DELETE'])
def delete_statistics(stat_id):
    success = StatisticsService.delete_one(stat_id)
    if success:
        return jsonify({"message": "Statistics record deleted successfully"}), 200
    return jsonify({"error": "Statistics record not found"}), 404

@statistics_controller.route('/delete-all', methods=['DELETE'])
def delete_all_statistics():
    StatisticsService.delete_all()
    return jsonify({"message": "All statistics records deleted successfully"}), 200

