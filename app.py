from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
import os

# Initialize Flask app
app = Flask(__name__)

# Configurations (these could be from environment variables)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/myDatabase")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your-secret-key")

# Enable CORS
CORS(app)

# Initialize PyMongo
mongo = PyMongo(app)

# Import routes (adjusted based on your structure)
from app.routes import main_routes  # or from app.routes import main_routes

# Register blueprints
app.register_blueprint(main_routes.bp)

if __name__ == "__main__":
    app.run(debug=True)
