from flask import Blueprint, request, jsonify, send_file, url_for
from src.modules.file_system.file_system_service import FileSystemService
from src.modules.file_system.file_system_dtos import UploadFileBody
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from werkzeug.utils import secure_filename
from io import BytesIO

file_system_controller = Blueprint('file_system', __name__)

@file_system_controller.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        # Get user ID from the JWT token
        user_id = get_jwt_identity()
        
        # Parse JSON data for folder_name
        folder_name = request.form.get("folder_name", "default")

        # Get the file from the form data
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        filename = secure_filename(file.filename)

        # Upload the file
        file_id = FileSystemService.upload_file(
            user_id=user_id,
            folder_name=folder_name,
            file_data=file.read(),
            filename=filename,
            content_type=file.content_type
        )

        if file_id:
            return jsonify({"message": "File uploaded successfully", "file_id": file_id}), 201
        else:
            return jsonify({"error": "File upload failed"}), 500

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@file_system_controller.route('/list-files', methods=['GET'])
@jwt_required()
def list_files():
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()
        
        # Get folder_name from query parameters (optional)
        folder_name = request.args.get("folder_name", "default")

        # Retrieve files by user ID and folder name
        files = FileSystemService.get_files_by_user_and_folder(user_id, folder_name)
        return jsonify(files), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@file_system_controller.route('/download/<file_id>', methods=['GET'])
@jwt_required()
def download_file(file_id):
    try:
        # Fetch the file from GridFS
        file = FileSystemService.download_file(file_id)
        if file:
            return send_file(BytesIO(file.read()), as_attachment=True, download_name=file.filename, mimetype=file.content_type)
        else:
            return jsonify({"error": "File not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@file_system_controller.route('/file/<file_id>', methods=['GET'])
def get_file_by_id(file_id):
    """
    Provides direct access to a file using its file_id.
    """
    try:
        # Fetch the file from GridFS
        file = FileSystemService.download_file(file_id)
        if file:
            # Return the file as an HTTP response
            return send_file(BytesIO(file.read()), download_name=file.filename, mimetype=file.content_type)
        else:
            return jsonify({"error": "File not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@file_system_controller.route('/file-url/<file_id>', methods=['GET'])
@jwt_required()
def get_file_url(file_id):
    """
    Provides a direct URL to access a file.
    """
    try:
        # Get the URL using Flask's url_for function
        file_url = url_for('file_system.get_file_by_id', file_id=file_id, _external=True)
        return jsonify({"file_url": file_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@file_system_controller.route('/recent-files', methods=['GET'])
@jwt_required()
def get_recent_files():
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()

        # Retrieve the top 5 most recent files for the user
        recent_files = FileSystemService.get_recent_files_by_user(user_id)
        return jsonify(recent_files), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@file_system_controller.route('/create-folder', methods=['POST'])
@jwt_required()
def create_folder():
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()

        # Get folder_name from request data
        folder_name = request.json.get("folder_name")
        if not folder_name:
            return jsonify({"error": "Folder name is required"}), 400

        # Create the folder
        result = FileSystemService.create_folder(user_id, folder_name)
        if result == "Folder created successfully":
            return jsonify({"message": result}), 201
        elif result == "Folder already exists":
            return jsonify({"message": result}), 409
        else:
            return jsonify({"error": "Failed to create folder"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@file_system_controller.route('/list-folders', methods=['GET'])
@jwt_required()
def list_folders():
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()

        # Retrieve the user's folder list
        folders = FileSystemService.get_user_folders(user_id)
        return jsonify(folders), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500