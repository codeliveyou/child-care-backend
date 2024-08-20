from src.modules.user.user_dtos import CreateUserBody, UpdateUserBody
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from constants import Constants

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class UserService:

    @staticmethod
    def create(body: CreateUserBody):
        user = body.model_dump()  # Using model_dump() instead of dict()
        user["created_at"] = datetime.utcnow()
        user["updated_at"] = datetime.utcnow()
        result = db.users.insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    def get_one(user_id: str):
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])  # Convert ObjectId to string
                if user.get('user_company_id'):
                    user['user_company_id'] = str(user['user_company_id'])  # Convert company ObjectId to string if present
            return user
        except Exception as e:
            # Log the exception
            print(f"Error fetching user: {e}")
            return None


    @staticmethod
    def get_all():
        try:
            users = list(db.users.find())
            for user in users:
                user['_id'] = str(user['_id'])  # Convert ObjectId to string
                user['user_company_id'] = str(user['user_company_id']) if user.get('user_company_id') else None  # Convert company ObjectId if present
            return users
        except Exception as e:
            # Log the exception
            print(f"Error fetching users: {e}")
            return []


    @staticmethod
    def update_one(user_id: str, body: UpdateUserBody):
        try:
            updates = {k: v for k, v in body.model_dump().items() if v is not None}
            updates["updated_at"] = datetime.utcnow()
            result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})
            if result.matched_count > 0:
                updated_user = db.users.find_one({"_id": ObjectId(user_id)})
                if updated_user:
                    updated_user['_id'] = str(updated_user['_id'])
                    if updated_user.get('user_company_id'):
                        updated_user['user_company_id'] = str(updated_user['user_company_id'])
                return updated_user
            return None
        except Exception as e:
            # Log the exception
            print(f"Error updating user: {e}")
            return None


    @staticmethod
    def delete_one(user_id: str):
        db.users.delete_one({"_id": ObjectId(user_id)})
        return True

    @staticmethod
    def delete_all():
        db.users.delete_many({})
        return True
