from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from src.modules.user_activity.user_activity_dtos import CreateUserActivityBody, UpdateUserActivityBody
from constants import Constants

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class UserActivityService:

    @staticmethod
    def create(body: CreateUserActivityBody):
        # Convert user_id to ObjectId
        user_id = ObjectId(body.user_id)

        # Prepare activity data for insertion
        activity_data = {
            "user_id": user_id,
            "login_time": body.login_time,
            "logout_time": body.logout_time,
            "activity_duration": None  # Calculated upon logout
        }

        # Insert activity into the database
        result = db.user_activity.insert_one(activity_data)
        return str(result.inserted_id)

    @staticmethod
    def get_one(id):
        activity = db.user_activity.find_one({"_id": ObjectId(id)})
        if activity:
            activity['_id'] = str(activity['_id'])
            activity['user_id'] = str(activity['user_id'])
        return activity

    @staticmethod
    def get_all():
        activities = list(db.user_activity.find())
        for activity in activities:
            activity['_id'] = str(activity['_id'])
            activity['user_id'] = str(activity['user_id'])
        return activities

    @staticmethod
    def update_one(id, body: UpdateUserActivityBody):
        # Find the user activity
        activity = db.user_activity.find_one({"_id": ObjectId(id)})
        if not activity:
            return None

        # Calculate activity duration if logout_time is provided
        if body.logout_time and activity["login_time"]:
            login_time = activity["login_time"]
            activity_duration = (body.logout_time - login_time).total_seconds()

            # Update the activity record
            update_data = {
                "logout_time": body.logout_time,
                "activity_duration": activity_duration
            }

            db.user_activity.update_one({"_id": ObjectId(id)}, {"$set": update_data})

            # Fetch updated activity
            updated_activity = db.user_activity.find_one({"_id": ObjectId(id)})
            updated_activity['_id'] = str(updated_activity['_id'])
            updated_activity['user_id'] = str(updated_activity['user_id'])
            return updated_activity

        return None

    @staticmethod
    def delete_one(id):
        db.user_activity.delete_one({"_id": ObjectId(id)})
        return True

    @staticmethod
    def delete_all():
        db.user_activity.delete_many({})
        return True
