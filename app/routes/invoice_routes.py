from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo

invoice_blueprint = Blueprint('invoice_blueprint', __name__)

@invoice_blueprint.route('/', methods=['POST'])
def create_invoice():
    data = request.get_json()
    invoice = {
        "company_id": ObjectId(data['company_id']),
        "amount": data['amount'],
        "status": data['status'],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = mongo.db.invoices.insert_one(invoice)
    return jsonify({"_id": str(result.inserted_id)}), 201

@invoice_blueprint.route('/', methods=['GET'])
def get_invoices():
    invoices = list(mongo.db.invoices.find())
    for invoice in invoices:
        invoice['_id'] = str(invoice['_id'])
        invoice['company_id'] = str(invoice['company_id'])
    return jsonify(invoices), 200

@invoice_blueprint.route('/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    invoice = mongo.db.invoices.find_one({"_id": ObjectId(invoice_id)})
    if invoice:
        invoice['_id'] = str(invoice['_id'])
        invoice['company_id'] = str(invoice['company_id'])
        return jsonify(invoice), 200
    return jsonify({"error": "Invoice not found"}), 404

@invoice_blueprint.route('/<invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    data = request.get_json()
    update_data = {
        "amount": data.get('amount'),
        "status": data.get('status'),
        "updated_at": datetime.utcnow()
    }
    mongo.db.invoices.update_one({"_id": ObjectId(invoice_id)}, {"$set": update_data})
    return jsonify({"message": "Invoice updated successfully"}), 200

@invoice_blueprint.route('/<invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    mongo.db.invoices.delete_one({"_id": ObjectId(invoice_id)})
    return jsonify({"message": "Invoice deleted successfully"}), 200

@invoice_blueprint.route('/company/<company_id>', methods=['GET'])
def get_invoices_by_company(company_id):
    invoices = list(mongo.db.invoices.find({"company_id": ObjectId(company_id)}))
    for invoice in invoices:
        invoice['_id'] = str(invoice['_id'])
        invoice['company_id'] = str(invoice['company_id'])
    return jsonify(invoices), 200
