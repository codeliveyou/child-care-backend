import boto3
from botocore.exceptions import NoCredentialsError
from constants import Constants


# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=Constants.AWS_ACCESS_KEY,
    aws_secret_access_key=Constants.AWS_SECRET_KEY
)

def upload_to_s3(file_path, s3_file_name, bucket_name = Constants.BUCKET_NAME):
    try:
        s3.upload_file(file_path, bucket_name, s3_file_name)
        print(f"Upload successful: {s3_file_name}")
        
        # Construct the URL to access the uploaded file
        data_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"
        return data_url
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def download_from_s3(s3_file_name, download_path, bucket_name = Constants.BUCKET_NAME):
    try:
        s3.download_file(bucket_name, s3_file_name, download_path)
        print(f"Download successful: {download_path}")
        return True
    except Exception as e:
        print(f"Download failed: {str(e)}")
        return False

def delete_from_s3(s3_file_name, bucket_name = Constants.BUCKET_NAME):
    try:
        s3.delete_object(Bucket=bucket_name, Key=s3_file_name)
        print(f"Deletion successful: {s3_file_name}")
        return True
    except Exception as e:
        print(f"Deletion failed: {str(e)}")
        return False
