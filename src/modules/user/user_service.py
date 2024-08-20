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
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
        return user

    @staticmethod
    def get_all():
        users = list(db.users.find())
        for user in users:
            user['_id'] = str(user['_id'])
        return users

    @staticmethod
    def update_one(user_id: str, body: UpdateUserBody):
        updates = {k: v for k, v in body.model_dump().items() if v is not None}
        updates["updated_at"] = datetime.utcnow()
        db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})
        return db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def delete_one(user_id: str):
        db.users.delete_one({"_id": ObjectId(user_id)})
        return True

    @staticmethod
    def delete_all():
        db.users.delete_many({})
        return True
