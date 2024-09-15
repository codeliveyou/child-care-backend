from pymongo import MongoClient
from bson.objectid import ObjectId
from constants import Constants
from datetime import datetime

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class CompanyActivityService:

    @staticmethod
    def aggregate_company_activity():
        # Aggregate total activity duration for each company based on user activities
        pipeline = [
            {
                "$lookup": {
                    "from": "users",  # Join with users collection to get company_id
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_info"
                }
            },
            {
                "$unwind": "$user_info"
            },
            {
                "$group": {
                    "_id": "$user_info.user_company_id",  # Group by company_id
                    "total_activity_duration": {
                        "$sum": "$activity_duration"  # Sum up activity durations
                    }
                }
            }
        ]

        # Run the aggregation on the user_activity table
        aggregated_results = db.user_activity.aggregate(pipeline)

        # Update the company_activity table with aggregated results
        for result in aggregated_results:
            company_id = result['_id']
            total_activity_duration = result['total_activity_duration']

            # Check if the company already has an activity record
            existing_record = db.company_activity.find_one({"company_id": company_id})

            if existing_record:
                # Update existing company activity record
                db.company_activity.update_one(
                    {"company_id": company_id},
                    {"$set": {"total_activity_duration": total_activity_duration}}
                )
            else:
                # Create new company activity record
                db.company_activity.insert_one({
                    "company_id": company_id,
                    "total_activity_duration": total_activity_duration
                })

        return "Company activity aggregation completed."

    @staticmethod
    def create(body):
        return f"create Company_activity"

    @staticmethod
    def get_one(id):
        company_activity = db.company_activity.find_one({"_id": ObjectId(id)})
        if company_activity:
            company_activity['_id'] = str(company_activity['_id'])
        return company_activity

    @staticmethod
    def get_all():
        company_activities = list(db.company_activity.find())
        for activity in company_activities:
            activity['_id'] = str(activity['_id'])
        return company_activities

    @staticmethod
    def update_one(id, body):
        return "update one Company_activity"

    @staticmethod
    def delete_one(id):
        db.company_activity.delete_one({"_id": ObjectId(id)})
        return "Company activity deleted"

    @staticmethod
    def delete_all():
        db.company_activity.delete_many({})
        return "All company activities deleted"
