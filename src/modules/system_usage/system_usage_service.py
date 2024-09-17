from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from src.modules.system_usage.system_usage_dtos import CreateSystemUsageBody, UpdateSystemUsageBody
from constants import Constants

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class SystemUsageService:

    @staticmethod
    def create(body: CreateSystemUsageBody):
        # Prepare system usage data for insertion
        usage_data = body.dict()
        usage_data['created_at'] = datetime.utcnow()
        usage_data['updated_at'] = datetime.utcnow()

        # Insert system usage data into the collection
        result = db.system_usage.insert_one(usage_data)
        return str(result.inserted_id)

    @staticmethod
    def get_one(id: str):
        # Fetch system usage by ID
        usage = db.system_usage.find_one({"_id": ObjectId(id)})
        if usage:
            usage['_id'] = str(usage['_id'])
        return usage

    @staticmethod
    def get_all():
        # Fetch all system usage records
        usages = list(db.system_usage.find())
        for usage in usages:
            usage['_id'] = str(usage['_id'])
        return usages

    @staticmethod
    def update_one(id: str, body: UpdateSystemUsageBody):
        # Prepare the update fields
        updates = {k: v for k, v in body.dict().items() if v is not None}
        updates['updated_at'] = datetime.utcnow()

        # Update the system usage record
        result = db.system_usage.update_one({"_id": ObjectId(id)}, {"$set": updates})
        if result.matched_count > 0:
            updated_usage = db.system_usage.find_one({"_id": ObjectId(id)})
            if updated_usage:
                updated_usage['_id'] = str(updated_usage['_id'])
            return updated_usage
        return None

    @staticmethod
    def delete_one(id: str):
        # Delete the system usage record by ID
        db.system_usage.delete_one({"_id": ObjectId(id)})
        return True

    @staticmethod
    def delete_all():
        # Delete all system usage records
        db.system_usage.delete_many({})
        return True
    
    @staticmethod
    def get_aggregated_system_usage(start_date: datetime = None, end_date: datetime = None):
        # Build the query to filter by date range
        query = {}
        if start_date and end_date:
            query["date"] = {"$gte": start_date, "$lte": end_date}

        # Fetch the filtered system usage records
        system_usages = list(db.system_usage.find(query))

        # Aggregate statistics
        total_users = sum([usage['total_users'] for usage in system_usages])
        active_users = sum([usage['active_users'] for usage in system_usages])
        total_sessions = sum([usage['total_sessions'] for usage in system_usages])
        total_duration = sum([usage['average_session_duration'] * usage['total_sessions'] for usage in system_usages])

        # Calculate average session duration across all records
        average_session_duration = (total_duration / total_sessions) if total_sessions > 0 else 0

        # Calculate trends over time (optional, could be basic statistics like the first and last day stats)
        trends = {
            "first_day_users": system_usages[0]['total_users'] if system_usages else 0,
            "last_day_users": system_usages[-1]['total_users'] if system_usages else 0,
            "first_day_sessions": system_usages[0]['total_sessions'] if system_usages else 0,
            "last_day_sessions": system_usages[-1]['total_sessions'] if system_usages else 0
        }

        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_sessions": total_sessions,
            "average_session_duration": average_session_duration,
            "trends": trends
        }