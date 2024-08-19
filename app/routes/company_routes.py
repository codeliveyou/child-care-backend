from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo
import random
import string

company_blueprint = Blueprint('company_blueprint', __name__)

@company_blueprint.route('/', methods=['POST'])
def create_company():
    data = request.get_json()
    company = {
        "company_name": data['company_name'],
        "company_description": data['company_description'],
        "company_email": data['company_email'],
        "company_contact_info": data['company_contact_info'],
        "company_payment_options": data['company_payment_options'],
        "company_code": ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = mongo.db.companies.insert_one(company)
    return jsonify({"_id": str(result.inserted_id)}), 201

@company_blueprint.route('/', methods=['GET'])
def get_companies():
    companies = list(mongo.db.companies.find())
    for company in companies:
        company['_id'] = str(company['_id'])
    return jsonify(companies), 200

@company_blueprint.route('/<company_id>', methods=['GET'])
def get_company(company_id):
    company = mongo.db.companies.find_one({"_id": ObjectId(company_id)})
    if company:
        company['_id'] = str(company['_id'])
        return jsonify(company), 200
    return jsonify({"error": "Company not found"}), 404

@company_blueprint.route('/<company_id>', methods=['PUT'])
def update_company(company_id):
    data = request.get_json()
    update_data = {
        "company_name": data.get('company_name'),
        "company_description": data.get('company_description'),
        "company_email": data.get('company_email'),
        "company_contact_info": data.get('company_contact_info'),
        "company_payment_options": data.get('company_payment_options'),
        "updated_at": datetime.utcnow()
    }
    mongo.db.companies.update_one({"_id": ObjectId(company_id)}, {"$set": update_data})
    return jsonify({"message": "Company updated successfully"}), 200

@company_blueprint.route('/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    mongo.db.companies.delete_one({"_id": ObjectId(company_id)})
    return jsonify({"message": "Company deleted successfully"}), 200
