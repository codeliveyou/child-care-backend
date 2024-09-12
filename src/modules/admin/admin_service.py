from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from constants import Constants
from src.modules.admin.admin_dtos import CreateAdminBody, UpdateAdminBody
import bcrypt
import jwt

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class AdminService:

    @staticmethod
    def create(body: CreateAdminBody):
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(body.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create admin dict with hashed password
        admin = {
            "admin_name": body.admin_name,
            "email": body.email,
            "password_hash": hashed_password,  # Store hashed password
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

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

            # If password is being updated, hash the new password
            if updates.get("password"):
                updates["password_hash"] = bcrypt.hashpw(updates["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                del updates["password"]  # Remove the plain text password

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

    @staticmethod
    def login(email, password):
        try:
            # Find the admin by email
            admin = db.admins.find_one({"email": email})
            if not admin:
                return None, "Admin not found"

            # Verify the password
            if not bcrypt.checkpw(password.encode('utf-8'), admin['password_hash'].encode('utf-8')):
                return None, "Invalid password"

            # Generate JWT token if login is successful
            token = jwt.encode({
                'admin_id': str(admin['_id']),
                'exp': datetime.utcnow() + timedelta(hours=2)  # Token valid for 2 hours
            }, 'your_secret_key', algorithm='HS256')

            return token, None

        except Exception as e:
            print(f"Error during admin login: {e}")
            return None, "Internal server error"
    
