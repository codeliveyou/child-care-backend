from src.modules.statistics.statistics_dtos import CreateStatisticsBody, UpdateStatisticsBody
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from constants import Constants

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class StatisticsService:

    @staticmethod
    def create(body: CreateStatisticsBody):
        stats = body.model_dump()
        stats["created_at"] = datetime.utcnow()
        stats["updated_at"] = datetime.utcnow()
        result = db.statistics.insert_one(stats)
        return str(result.inserted_id)

    @staticmethod
    def get_one(stat_id: str):
        try:
            stat = db.statistics.find_one({"_id": ObjectId(stat_id)})
            if stat:
                stat['_id'] = str(stat['_id'])
                stat['company_id'] = str(stat['company_id'])
                if stat.get('user_id'):
                    stat['user_id'] = str(stat['user_id'])
            return stat
        except Exception as e:
            # Log the exception
            print(f"Error fetching statistics: {e}")
            return None

    @staticmethod
    def get_all():
        try:
            stats = list(db.statistics.find())
            for stat in stats:
                stat['_id'] = str(stat['_id'])
                stat['company_id'] = str(stat['company_id'])
                if stat.get('user_id'):
                    stat['user_id'] = str(stat['user_id'])
            return stats
        except Exception as e:
            # Log the exception
            print(f"Error fetching statistics: {e}")
            return []

    @staticmethod
    def update_one(stat_id: str, body: UpdateStatisticsBody):
        try:
            updates = {k: v for k, v in body.model_dump().items() if v is not None}
            updates["updated_at"] = datetime.utcnow()
            result = db.statistics.update_one({"_id": ObjectId(stat_id)}, {"$set": updates})
            if result.matched_count > 0:
                updated_stat = db.statistics.find_one({"_id": ObjectId(stat_id)})
                if updated_stat:
                    updated_stat['_id'] = str(updated_stat['_id'])
                    updated_stat['company_id'] = str(updated_stat['company_id'])
                    if updated_stat.get('user_id'):
                        updated_stat['user_id'] = str(updated_stat['user_id'])
                return updated_stat
            return None
        except Exception as e:
            # Log the exception
            print(f"Error updating statistics: {e}")
            return None

    @staticmethod
    def delete_one(stat_id: str):
        db.statistics.delete_one({"_id": ObjectId(stat_id)})
        return True

    @staticmethod
    def delete_all():
        db.statistics.delete_many({})
        return True

