from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['avatar_platform']

class Statistics:
    def __init__(self, company_id, time_spent, sessions_count, rooms_count, user_id=None):
        self.company_id = ObjectId(company_id)
        self.user_id = ObjectId(user_id) if user_id else None
        self.time_spent = time_spent
        self.sessions_count = sessions_count
        self.rooms_count = rooms_count
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        return db.statistics.insert_one({
            "company_id": self.company_id,
            "user_id": self.user_id,
            "time_spent": self.time_spent,
            "sessions_count": self.sessions_count,
            "rooms_count": self.rooms_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        })

    @staticmethod
    def find_by_id(stat_id):
        return db.statistics.find_one({"_id": ObjectId(stat_id)})

    @staticmethod
    def find_by_company(company_id):
        return db.statistics.find({"company_id": ObjectId(company_id)})

    @staticmethod
    def find_by_user(user_id):
        return db.statistics.find({"user_id": ObjectId(user_id)})

    @staticmethod
    def update_stat(stat_id, updates):
        updates['updated_at'] = datetime.utcnow()
        db.statistics.update_one({"_id": ObjectId(stat_id)}, {"$set": updates})

    @staticmethod
    def delete_stat(stat_id):
        db.statistics.delete_one({"_id": ObjectId(stat_id)})
