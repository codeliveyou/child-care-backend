from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from constants import Constants
from src.modules.invoice.invoice_dtos import CreateInvoiceBody, UpdateInvoiceBody

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class InvoiceService:

    @staticmethod
    def create(body: CreateInvoiceBody):
        try:
            invoice = body.dict()
            invoice["created_at"] = datetime.utcnow()
            invoice["updated_at"] = datetime.utcnow()
            result = db.invoices.insert_one(invoice)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating invoice: {e}")
            return None

    @staticmethod
    def get_one(invoice_id: str):
        try:
            invoice = db.invoices.find_one({"_id": ObjectId(invoice_id)})
            if invoice:
                invoice['_id'] = str(invoice['_id'])  # Convert ObjectId to string
                invoice['company_id'] = str(invoice['company_id'])  # Convert ObjectId to string
            return invoice
        except Exception as e:
            print(f"Error fetching invoice: {e}")
            return None

    @staticmethod
    def get_all():
        try:
            invoices = list(db.invoices.find())
            for invoice in invoices:
                invoice['_id'] = str(invoice['_id'])  # Convert ObjectId to string
                invoice['company_id'] = str(invoice['company_id'])  # Convert ObjectId to string
            return invoices
        except Exception as e:
            print(f"Error fetching invoices: {e}")
            return []

    @staticmethod
    def update_one(invoice_id: str, body: UpdateInvoiceBody):
        try:
            updates = {k: v for k, v in body.dict().items() if v is not None}
            updates["updated_at"] = datetime.utcnow()
            result = db.invoices.update_one({"_id": ObjectId(invoice_id)}, {"$set": updates})
            if result.matched_count > 0:
                updated_invoice = db.invoices.find_one({"_id": ObjectId(invoice_id)})
                if updated_invoice:
                    updated_invoice['_id'] = str(updated_invoice['_id'])
                    updated_invoice['company_id'] = str(updated_invoice['company_id'])
                return updated_invoice
            return None
        except Exception as e:
            print(f"Error updating invoice: {e}")
            return None

    @staticmethod
    def delete_one(invoice_id: str):
        try:
            db.invoices.delete_one({"_id": ObjectId(invoice_id)})
            return True
        except Exception as e:
            print(f"Error deleting invoice: {e}")
            return False

    @staticmethod
    def delete_all():
        try:
            db.invoices.delete_many({})
            return True
        except Exception as e:
            print(f"Error deleting all invoices: {e}")
            return False
