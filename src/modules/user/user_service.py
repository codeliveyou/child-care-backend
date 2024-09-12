from src.modules.user.user_dtos import RegisterUserBody, CreateUserBody, UpdateUserBody
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from constants import Constants
import bcrypt
import jwt

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']

class UserService:

    @staticmethod
    def register(body: RegisterUserBody):
        # Hash the user's password before saving it
        hashed_password = bcrypt.hashpw(body.user_password.encode('utf-8'), bcrypt.gensalt())

        # Find the company using the company_code
        company = db.companies.find_one({"company_code": body.company_code})
        if not company:
            return None, "Invalid company code"

        # Prepare user data for storage
        user_data = {
            "user_name": body.user_name,
            "user_email": body.user_email,
            "user_password_hash": hashed_password.decode('utf-8'),  # Store hashed password
            "user_company_id": company['_id'],  # Associate user with company using ObjectId
            "user_role": "user",  # Default role
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Insert user into database
        result = db.users.insert_one(user_data)
        user_id = str(result.inserted_id)

        # Placeholder: Send confirmation email (implement actual email functionality)
        print(f"Sending confirmation email to {body.user_email}")

        return user_id, None
    
    @staticmethod
    def create(body: CreateUserBody):
        # Hash the user's password before saving it
        hashed_password = bcrypt.hashpw(body.user_password_hash.encode('utf-8'), bcrypt.gensalt())

        user = body.model_dump()
        user['user_password_hash'] = hashed_password.decode('utf-8')  # Store as a string
        user["created_at"] = datetime.utcnow()
        user["updated_at"] = datetime.utcnow()
        result = db.users.insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    def get_one(user_id: str):
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])  # Convert ObjectId to string
                if user.get('user_company_id'):
                    user['user_company_id'] = str(user['user_company_id'])  # Convert company ObjectId to string if present
            return user
        except Exception as e:
            # Log the exception
            print(f"Error fetching user: {e}")
            return None


    @staticmethod
    def get_all(page: int = 1, page_size: int = 10):
        """Fetch all users with pagination"""
        try:
            # Calculate the offset based on page and page_size
            skip = (page - 1) * page_size

            # Fetch paginated users
            users = list(db.users.find().skip(skip).limit(page_size))
            
            # Convert ObjectIds and other fields to strings
            for user in users:
                user['_id'] = str(user['_id'])  # Convert ObjectId to string
                user['user_company_id'] = str(user['user_company_id']) if user.get('user_company_id') else None  # Convert company ObjectId if present

            # Get the total user count for pagination metadata
            total_users = db.users.count_documents({})

            return {
                "users": users,
                "total_users": total_users,
                "page": page,
                "page_size": page_size,
                "total_pages": (total_users + page_size - 1) // page_size  # Calculate total pages
            }
        except Exception as e:
            # Log the exception
            print(f"Error fetching users: {e}")
            return {
                "users": [],
                "total_users": 0,
                "page": page,
                "page_size": page_size,
                "total_pages": 0
            }


    @staticmethod
    def update_one(user_id: str, body: UpdateUserBody):
        try:
            updates = {k: v for k, v in body.model_dump().items() if v is not None}
            updates["updated_at"] = datetime.utcnow()
            result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})
            if result.matched_count > 0:
                updated_user = db.users.find_one({"_id": ObjectId(user_id)})
                if updated_user:
                    updated_user['_id'] = str(updated_user['_id'])
                    if updated_user.get('user_company_id'):
                        updated_user['user_company_id'] = str(updated_user['user_company_id'])
                return updated_user
            return None
        except Exception as e:
            # Log the exception
            print(f"Error updating user: {e}")
            return None


    @staticmethod
    def delete_one(user_id: str):
        db.users.delete_one({"_id": ObjectId(user_id)})
        return True

    @staticmethod
    def delete_all():
        db.users.delete_many({})
        return True

    @staticmethod
    def login(email, password):
        try:
            # Log the input email and password
            print(f"Attempting to log in with email: {email}")

            # Find the user by email
            user = db.users.find_one({"user_email": email})
            if not user:
                print("User not found")
                return None, "User not found"

            # Log the found user information
            print(f"User found: {user}")

            # Verify the password using bcrypt
            if not bcrypt.checkpw(password.encode('utf-8'), user['user_password_hash'].encode('utf-8')):
                print("Password check failed")
                return None, "Invalid password"

            # Generate JWT token if login is successful
            token = jwt.encode({
                'user_id': str(user['_id']),
                'exp': datetime.utcnow() + timedelta(hours=2)  # Token valid for 2 hours
            }, 'your_secret_key', algorithm='HS256')

            print("Login successful, token generated")
            return token, None

        except Exception as e:
            print(f"Error during login: {e}")
            return None, "Internal server error"
