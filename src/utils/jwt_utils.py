# src/utils/jwt_utils.py
import jwt
from flask import request

SECRET_KEY = 'your_secret_key'

def generate_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
