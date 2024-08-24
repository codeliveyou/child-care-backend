import boto3
from botocore.exceptions import NoCredentialsError

# AWS credentials and bucket name
AWS_ACCESS_KEY = 'your-access-key-id'
AWS_SECRET_KEY = 'your-secret-access-key'
BUCKET_NAME = 'your-bucket-name'

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def upload_to_s3(file_path, bucket_name, s3_file_name):
    try:
        s3.upload_file(file_path, bucket_name, s3_file_name)
        print(f"Upload successful: {s3_file_name}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def download_from_s3(s3_file_name, bucket_name, download_path):
    try:
        s3.download_file(bucket_name, s3_file_name, download_path)
        print(f"Download successful: {download_path}")
        return True
    except Exception as e:
        print(f"Download failed: {str(e)}")
        return False
