from src.modules.user.user_dtos import RegisterUserBody, UpdateUserBody
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from constants import Constants
import bcrypt
from flask_jwt_extended import create_access_token
import gridfs
from io import BytesIO



client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']
fs = gridfs.GridFS(db)

class UserService:

    @staticmethod
    def register(body: RegisterUserBody):
        # Check if the email is already registered
        existing_user = db.users.find_one({"user_email": body.user_email})
        if existing_user:
            return None, "Email is already registered"

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
            "account_description": body.account_description,  # Include account description
            "profile_picture": "671a52662b5daf08caafc6b3",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Insert user into database
        result = db.users.insert_one(user_data)
        user_id = str(result.inserted_id)

        # Generate JWT token using Flask-JWT-Extended
        token = create_access_token(identity=user_id)

        # Placeholder: Send confirmation email (implement actual email functionality)
        print(f"Sending confirmation email to {body.user_email}")

        # Return the user ID and the token
        return user_id, token
    
    @staticmethod
    def change_profile_info(user_id: str, user_name: str, user_email: str, account_description: str):
        try:
            # Prepare the updates dictionary
            updates = {
                "user_name": user_name,
                "user_email": user_email,
                "account_description": account_description,
                "updated_at": datetime.utcnow()
            }

            # Update the user's profile information in the database
            result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})

            if result.matched_count > 0:
                return True, "Profile information updated successfully"
            return False, "Failed to update profile information"

        except Exception as e:
            print(f"Error updating profile info: {e}")
            return False, "Internal server error"

    @staticmethod
    def change_password(user_id: str, old_password: str, new_password: str):
        try:
            # Fetch the user from the database
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return False, "User not found"

            # Verify the old password using bcrypt
            if not bcrypt.checkpw(old_password.encode('utf-8'), user['user_password_hash'].encode('utf-8')):
                return False, "Old password is incorrect"

            # Hash the new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            # Update the user's password in the database
            result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {
                "user_password_hash": hashed_password.decode('utf-8'),
                "updated_at": datetime.utcnow()
            }})

            if result.matched_count > 0:
                return True, "Password updated successfully"
            return False, "Failed to update password"

        except Exception as e:
            print(f"Error changing password: {e}")
            return False, "Internal server error"

    @staticmethod
    def change_profile_picture(user_id: str, picture_data: bytes, filename: str):
        try:
            # Save the image to GridFS
            picture_id = fs.put(picture_data, filename=filename, content_type="image/jpeg")

            # Update the user's profile with the new profile picture ID
            result = db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"profile_picture": str(picture_id), "updated_at": datetime.utcnow()}}
            )

            if result.matched_count > 0:
                return True, str(picture_id)
            return False, None

        except Exception as e:
            print(f"Error changing profile picture: {e}")
            return False, None
    
    @staticmethod
    def get_profile_picture(picture_id: str):
        try:
            # Fetch the picture from GridFS
            picture = fs.get(ObjectId(picture_id))
            return picture

        except gridfs.errors.NoFile:
            return None

    @staticmethod
    def get_profile_picture_by_email(email: str):
        try:
            # Find the user by email
            user = db.users.find_one({"user_email": email})
            if not user:
                return None, "User not found"

            # Check if the user has a profile picture
            if not user.get("profile_picture"):
                return None, "No profile picture available"

            # Fetch the picture from GridFS using the picture ID
            picture_id = user.get("profile_picture")
            picture = fs.get(ObjectId(picture_id))

            return picture, None

        except gridfs.errors.NoFile:
            return None, "Profile picture not found"

        except Exception as e:
            print(f"Error fetching profile picture by email: {e}")
            return None, "Internal server error"

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
            print(f"Attempting to log in with email: {email}")

            # Find the user by email
            user = db.users.find_one({"user_email": email})
            if not user:
                print("User not found")
                return None, "User not found"

            # Verify the password using bcrypt
            if not bcrypt.checkpw(password.encode('utf-8'), user['user_password_hash'].encode('utf-8')):
                print("Password check failed")
                return None, "Invalid password"

            # Generate JWT token if login is successful
            token = create_access_token(identity=str(user['_id']))

            print(f"Login successful, token generated.")
            return token, None

        except Exception as e:
            print(f"Error during login: {e}")
            return None, "Internal server error"
    
    
    @staticmethod
    def logout(user_id):
        try:
            # Find the most recent login entry for the user (i.e., the one without a logout time)
            activity = db.user_activity.find_one({
                "user_id": ObjectId(user_id),
                "logout_time": None  # Ensure we only find the open session
            }, sort=[("login_time", -1)])  # Sort by login time to get the latest

            if not activity:
                return "No active session found for user."

            # Record the logout time
            logout_time = datetime.utcnow()

            # Calculate the activity duration (in seconds)
            login_time = activity["login_time"]
            activity_duration = (logout_time - login_time).total_seconds()

            # Update the user_activity log with logout_time and activity_duration
            update_data = {
                "logout_time": logout_time,
                "activity_duration": activity_duration
            }

            db.user_activity.update_one({"_id": activity["_id"]}, {"$set": update_data})

            print(f"Logout successful, activity duration: {activity_duration} seconds")
            return "Logout successful"

        except Exception as e:
            print(f"Error during logout: {e}")
            return "Internal server error"

    @staticmethod
    def get_users_by_company_id(company_id: str):
        """Fetch all users belonging to a specific company"""
        try:
            users = list(db.users.find({"user_company_id": ObjectId(company_id)}))
            
            # Format the users list
            formatted_users = []
            for user in users:
                formatted_users.append({
                    "user_name": user.get('user_name'),
                    "account_description": user.get('account_description', '-'),
                    "user_email": user.get('user_email', '-'),
                    "created_at": user.get('created_at').strftime("%d-%m-%Y") if user.get('created_at') else '-',
                    "use_time": "10h",  # Placeholder for use time
                    "status": "Active"  # Placeholder for status
                })
            
            return formatted_users

        except Exception as e:
            print(f"Error fetching users for company_id {company_id}: {e}")
            return []