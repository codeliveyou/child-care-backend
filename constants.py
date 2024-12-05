import os
from dotenv import load_dotenv

load_dotenv()


class Constants:
    PORT = os.environ.get('PORT') or 8000
    DATABASE_URL = os.environ.get('DATABASE_URL')
    PROD = os.environ.get('PROD') or None
    JWT_SECRET = os.environ.get('JWT_SECRET') or "SECRET"
    TOKEN_VALIDITY = os.environ.get('TOKEN_VALIDITY') or 7
    APP_NAME = os.environ.get('APP_NAME') or "APP"
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    BUCKET_NAME = os.environ.get('BUCKET_NAME')


    SMTP_SERVER = "smtp.gmail.com"  # Replace with your SMTP server
    SMTP_PORT = 587  # Replace with your SMTP port
    SMTP_USERNAME = "the.dream.is.close@gmail.com"  # Replace with your email address
    SMTP_PASSWORD = "534386"  # Replace with your email password
