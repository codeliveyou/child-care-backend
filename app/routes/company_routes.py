from flask import Flask, jsonify, request
from app.models.company import Company
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['avatar_platform']

@app.route('/api/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    new_company = Company(
        company_name=data['company_name'],
        company_description=data['company_description'],
        company_email=data['company_email'],
        company_contact_info=data['company_contact_info'],
        company_payment_options=data['company_payment_options'],
        company_code=data['company_code']
    )
    result = new_company.save()
    return jsonify({"_id": str(result.inserted_id)}), 201

@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = db.companies.find()
    return jsonify([{"_id": str(company["_id"]), "company_name": company["company_name"]} for company in companies])

@app.route('/api/companies/<company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.find_by_id(company_id)
    if company:
        company["_id"] = str(company["_id"])
        return jsonify(company)
    else:
        return jsonify({"error": "Company not found"}), 404

@app.route('/api/companies/<company_id>', methods=['PUT'])
def update_company(company_id):
    data = request.get_json()
    Company.update_company(company_id, data)
    return jsonify({"message": "Company updated successfully"}), 200

@app.route('/api/companies/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    Company.delete_company(company_id)
    return jsonify({"message": "Company deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
