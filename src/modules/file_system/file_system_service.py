from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
from datetime import datetime
from constants import Constants

client = MongoClient(Constants.DATABASE_URL)
db = client['CC-database']
fs = gridfs.GridFS(db)

class FileSystemService:

    @staticmethod
    def determine_file_type(filename: str) -> str:
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
        document_extensions = ['.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx']

        extension = filename.split('.')[-1].lower()
        if f".{extension}" in video_extensions:
            return "video"
        elif f".{extension}" in document_extensions:
            return "document"
        return "unknown"

    @staticmethod
    def upload_file(user_id: str, folder_name: str, file_data: bytes, filename: str, content_type: str):
        try:
            # Calculate file size in bytes
            file_size = len(file_data)

            # Determine file type
            file_type = FileSystemService.determine_file_type(filename)

            # Metadata for file tracking, including file size and type
            metadata = {
                "user_id": user_id,
                "folder_name": folder_name,
                "file_size": file_size,  # New file size field
                "file_directory": folder_name,  # Store directory name
                "file_type": file_type,  # Store file type
                "upload_date": datetime.utcnow()
            }

            # Store file in GridFS with metadata
            file_id = fs.put(file_data, filename=filename, metadata=metadata, content_type=content_type)
            return str(file_id)

        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

    @staticmethod
    def get_files_by_user_and_folder(user_id: str, folder_name: str):
        # Query GridFS for files matching user_id and folder_name
        files = fs.find({"metadata.user_id": user_id, "metadata.folder_name": folder_name})
        return [{
            "file_id": str(file._id),
            "filename": file.filename,
            "file_size": file.metadata.get("file_size", 0),  # Retrieve file size
            "upload_date": file.metadata["upload_date"],
            "file_directory": file.metadata.get("file_directory", ""),
            "file_type": file.metadata.get("file_type", "unknown")
        } for file in files]

    @staticmethod
    def download_file(file_id: str):
        try:
            # Retrieve file from GridFS by ID
            file = fs.get(ObjectId(file_id))
            return file
        except Exception as e:
            print(f"Error retrieving file: {e}")
            return None

    @staticmethod
    def get_recent_files_by_user(user_id: str, limit: int = 5):
        try:
            # Query GridFS for files matching the user_id and sort by upload_date (descending)
            files = fs.find({"metadata.user_id": user_id}).sort("metadata.upload_date", -1).limit(limit)
            return [{
                "file_id": str(file._id),
                "filename": file.filename,
                "file_size": file.metadata.get("file_size", 0),  # Retrieve file size
                "upload_date": file.metadata["upload_date"],
                "file_directory": file.metadata.get("file_directory", ""),
                "file_type": file.metadata.get("file_type", "unknown")
            } for file in files]

        except Exception as e:
            print(f"Error retrieving recent files: {e}")
            return []
    

    @staticmethod
    def create_folder(user_id: str, folder_name: str):
        try:
            # Check if the folder already exists for the user
            existing_folder = db['folders'].find_one({"user_id": user_id, "folder_name": folder_name})
            if existing_folder:
                return "Folder already exists"

            # Insert a new folder document
            db['folders'].insert_one({
                "user_id": user_id,
                "folder_name": folder_name,
                "created_date": datetime.utcnow()
            })
            return "Folder created successfully"

        except Exception as e:
            print(f"Error creating folder: {e}")
            return None

    @staticmethod
    def get_user_folders(user_id: str):
        try:
            # Retrieve all folders for the user
            folders = db['folders'].find({"user_id": user_id})
            return [{
                "folder_name": folder["folder_name"],
                "created_date": folder["created_date"]
            } for folder in folders]

        except Exception as e:
            print(f"Error retrieving folders: {e}")
            return []