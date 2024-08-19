from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient("mongodb://localhost:27017/")
db = client['avatar_platform']

class User:
    def __init__(self, username, email, password, company_id, role='regular_user'):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.company_id = ObjectId(company_id)
        self.role = role
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        return db.users.insert_one({
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "company_id": self.company_id,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        })

    @staticmethod
    def find_by_id(user_id):
        return db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({"email": email})

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def update_user(user_id, updates):
        updates['updated_at'] = datetime.utcnow()
        db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})

    @staticmethod
    def delete_user(user_id):
        db.users.delete_one({"_id": ObjectId(user_id)})
