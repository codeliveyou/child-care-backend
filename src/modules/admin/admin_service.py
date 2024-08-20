from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from constants import Constants
from src.modules.admin.admin_dtos import CreateAdminBody, UpdateAdminBody

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class AdminService:

    @staticmethod
    def create(body: CreateAdminBody):
        admin = body.dict()  # Convert Pydantic model to dictionary
        admin["created_at"] = datetime.utcnow()
        admin["updated_at"] = datetime.utcnow()
        result = db.admins.insert_one(admin)
        return str(result.inserted_id)

    @staticmethod
    def get_one(admin_id: str):
        try:
            admin = db.admins.find_one({"_id": ObjectId(admin_id)})
            if admin:
                admin['_id'] = str(admin['_id'])  # Convert ObjectId to string
            return admin
        except Exception as e:
            print(f"Error fetching admin: {e}")
            return None

    @staticmethod
    def get_all():
        try:
            admins = list(db.admins.find())
            for admin in admins:
                admin['_id'] = str(admin['_id'])  # Convert ObjectId to string
            return admins
        except Exception as e:
            print(f"Error fetching admins: {e}")
            return []

    @staticmethod
    def update_one(admin_id: str, body: UpdateAdminBody):
        try:
            updates = {k: v for k, v in body.dict().items() if v is not None}
            updates["updated_at"] = datetime.utcnow()
            result = db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": updates})
            if result.matched_count > 0:
                updated_admin = db.admins.find_one({"_id": ObjectId(admin_id)})
                if updated_admin:
                    updated_admin['_id'] = str(updated_admin['_id'])
                return updated_admin
            return None
        except Exception as e:
            print(f"Error updating admin: {e}")
            return None

    @staticmethod
    def delete_one(admin_id: str):
        db.admins.delete_one({"_id": ObjectId(admin_id)})
        return True

    @staticmethod
    def delete_all():
        db.admins.delete_many({})
        return True
