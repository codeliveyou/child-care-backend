from flask import Blueprint, request, jsonify
from src.modules.invoice.invoice_service import InvoiceService
from src.modules.invoice.invoice_dtos import CreateInvoiceBody, UpdateInvoiceBody
from pydantic import ValidationError

invoice_controller = Blueprint('invoices', __name__)

@invoice_controller.route('/', methods=['POST'])
def create_invoice():
    try:
        data = request.get_json()
        body = CreateInvoiceBody(**data)
        invoice_id = InvoiceService.create(body)
        if invoice_id:
            return jsonify({"_id": invoice_id}), 201
        return jsonify({"error": "Failed to create invoice"}), 500
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        print(f"Error in create_invoice: {e}")
        return jsonify({"error": str(e)}), 500

@invoice_controller.route('/', methods=['GET'])
def get_invoices():
    try:
        invoices = InvoiceService.get_all()
        return jsonify(invoices), 200
    except Exception as e:
        print(f"Error in get_invoices: {e}")
        return jsonify({"error": str(e)}), 500

@invoice_controller.route('/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    try:
        invoice = InvoiceService.get_one(invoice_id)
        if invoice:
            return jsonify(invoice), 200
        return jsonify({"error": "Invoice not found"}), 404
    except Exception as e:
        print(f"Error in get_invoice: {e}")
        return jsonify({"error": str(e)}), 500

@invoice_controller.route('/<invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    try:
        data = request.get_json()
        body = UpdateInvoiceBody(**data)
        updated_invoice = InvoiceService.update_one(invoice_id, body)
        if updated_invoice:
            return jsonify(updated_invoice), 200
        return jsonify({"error": "Invoice not found"}), 404
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        print(f"Error in update_invoice: {e}")
        return jsonify({"error": str(e)}), 500

@invoice_controller.route('/<invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    try:
        success = InvoiceService.delete_one(invoice_id)
        if success:
            return jsonify({"message": "Invoice deleted successfully"}), 200
        return jsonify({"error": "Invoice not found"}), 404
    except Exception as e:
        print(f"Error in delete_invoice: {e}")
        return jsonify({"error": str(e)}), 500

@invoice_controller.route('/delete-all', methods=['DELETE'])
def delete_all_invoices():
    try:
        InvoiceService.delete_all()
        return jsonify({"message": "All invoices deleted successfully"}), 200
    except Exception as e:
        print(f"Error in delete_all_invoices: {e}")
        return jsonify({"error": str(e)}), 500
