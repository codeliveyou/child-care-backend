from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['avatar_platform']

class Invoice:
    def __init__(self, company_id, amount, status="pending"):
        self.company_id = ObjectId(company_id)
        self.amount = amount
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        return db.invoices.insert_one({
            "company_id": self.company_id,
            "amount": self.amount,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        })

    @staticmethod
    def find_by_id(invoice_id):
        return db.invoices.find_one({"_id": ObjectId(invoice_id)})

    @staticmethod
    def find_by_company(company_id):
        return db.invoices.find({"company_id": ObjectId(company_id)})

    @staticmethod
    def update_invoice(invoice_id, updates):
        updates['updated_at'] = datetime.utcnow()
        db.invoices.update_one({"_id": ObjectId(invoice_id)}, {"$set": updates})

    @staticmethod
    def delete_invoice(invoice_id):
        db.invoices.delete_one({"_id": ObjectId(invoice_id)})
