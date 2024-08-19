from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['avatar_platform']

class Company:
    def __init__(self, company_name, company_description, company_email, company_contact_info, company_payment_options, company_code):
        self.company_name = company_name
        self.company_description = company_description
        self.company_email = company_email
        self.company_contact_info = company_contact_info
        self.company_payment_options = company_payment_options
        self.company_code = company_code
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        return db.companies.insert_one({
            "company_name": self.company_name,
            "company_description": self.company_description,
            "company_email": self.company_email,
            "company_contact_info": self.company_contact_info,
            "company_payment_options": self.company_payment_options,
            "company_code": self.company_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        })

    @staticmethod
    def find_by_id(company_id):
        return db.companies.find_one({"_id": ObjectId(company_id)})

    @staticmethod
    def update_company(company_id, updates):
        updates['updated_at'] = datetime.utcnow()
        db.companies.update_one({"_id": ObjectId(company_id)}, {"$set": updates})

    @staticmethod
    def delete_company(company_id):
        db.companies.delete_one({"_id": ObjectId(company_id)})
