from src.modules.company.company_dtos import CreateCompanyBody, UpdateCompanyBody
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import random, string
from constants import Constants

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class CompanyService:

    @staticmethod
    def create(body: CreateCompanyBody):
        company = body.model_dump()  # Replaced dict() with model_dump()
        company["company_code"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        company["created_at"] = datetime.utcnow()
        company["updated_at"] = datetime.utcnow()
        result = db.companies.insert_one(company)
        return str(result.inserted_id)

    @staticmethod
    def get_one(company_id: str):
        company = db.companies.find_one({"_id": ObjectId(company_id)})
        if company:
            company['_id'] = str(company['_id'])
        return company

    @staticmethod
    def get_all():
        companies = list(db.companies.find())
        for company in companies:
            company['_id'] = str(company['_id'])
        return companies

    @staticmethod
    def update_one(company_id: str, body: UpdateCompanyBody):
        updates = {k: v for k, v in body.model_dump().items() if v is not None}
        updates["updated_at"] = datetime.utcnow()
        db.companies.update_one({"_id": ObjectId(company_id)}, {"$set": updates})
        return db.companies.find_one({"_id": ObjectId(company_id)})

    @staticmethod
    def delete_one(company_id: str):
        db.companies.delete_one({"_id": ObjectId(company_id)})
        return True

    @staticmethod
    def delete_all():
        db.companies.delete_many({})
        return True
