from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import MONGO_URI

# client = MongoClient("mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['admin']

class Admin:
    def __init__(self, admin_name, email, password):
        self.admin_name = admin_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        return db.admins.insert_one({
            "admin_name": self.admin_name,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        })

    @staticmethod
    def find_by_id(admin_id):
        return db.admins.find_one({"_id": ObjectId(admin_id)})

    @staticmethod
    def find_by_email(email):
        return db.admins.find_one({"email": email})

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def update_admin(admin_id, updates):
        updates['updated_at'] = datetime.utcnow()
        db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": updates})

    @staticmethod
    def delete_admin(admin_id):
        db.admins.delete_one({"_id": ObjectId(admin_id)})
