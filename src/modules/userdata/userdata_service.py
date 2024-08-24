from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from constants import Constants
from src.modules.userdata.userdata_dtos import CreateUserDataBody, UpdateUserDataBody

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class UserDataService:

    @staticmethod
    def create(body: CreateUserDataBody):
        try:
            userdata = body.dict()
            userdata["created_at"] = datetime.utcnow()
            userdata["updated_at"] = datetime.utcnow()
            result = db.userdata.insert_one(userdata)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating userdata: {e}")
            return None

    @staticmethod
    def get_one(userdata_id: str):
        try:
            userdata = db.userdata.find_one({"_id": ObjectId(userdata_id)})
            if userdata:
                userdata['_id'] = str(userdata['_id'])  # Convert ObjectId to string
                userdata['user_id'] = str(userdata['user_id'])  # Convert ObjectId to string
                userdata['data_url'] = str(userdata['data_url'])  # Convert ObjectId to string
                userdata['participants'] = [str(p) for p in userdata['participants']]  # Convert ObjectIds to string
            return userdata
        except Exception as e:
            print(f"Error fetching userdata: {e}")
            return None

    @staticmethod
    def get_all():
        try:
            userdata_list = list(db.userdata.find())
            for userdata in userdata_list:
                userdata['_id'] = str(userdata['_id'])  # Convert ObjectId to string
                userdata['user_id'] = str(userdata['user_id'])  # Convert ObjectId to string
                userdata['data_url'] = str(userdata['data_url'])  # Convert ObjectId to string
                userdata['participants'] = [str(p) for p in userdata['participants']]  # Convert ObjectIds to string
            return userdata_list
        except Exception as e:
            print(f"Error fetching userdata: {e}")
            return []

    @staticmethod
    def update_one(userdata_id: str, body: UpdateUserDataBody):
        try:
            updates = {k: v for k, v in body.dict().items() if v is not None}
            updates["updated_at"] = datetime.utcnow()
            result = db.userdata.update_one({"_id": ObjectId(userdata_id)}, {"$set": updates})
            if result.matched_count > 0:
                updated_userdata = db.userdata.find_one({"_id": ObjectId(userdata_id)})
                if updated_userdata:
                    updated_userdata['_id'] = str(updated_userdata['_id'])
                    updated_userdata['user_id'] = str(updated_userdata['user_id'])
                    updated_userdata['data_url'] = str(updated_userdata['data_url'])
                    updated_userdata['participants'] = [str(p) for p in updated_userdata['participants']]
                return updated_userdata
            return None
        except Exception as e:
            print(f"Error updating userdata: {e}")
            return None

    @staticmethod
    def delete_one(userdata_id: str):
        try:
            db.userdata.delete_one({"_id": ObjectId(userdata_id)})
            return True
        except Exception as e:
            print(f"Error deleting userdata: {e}")
            return False

    @staticmethod
    def delete_all():
        try:
            db.userdata.delete_many({})
            return True
        except Exception as e:
            print(f"Error deleting all userdata: {e}")
            return False
