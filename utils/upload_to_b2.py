import django
from django.conf import settings
import os
import sys
import boto3
from dotenv import load_dotenv
from django.conf import settings
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

# Set the Django settings module environment variable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eaglespoint.settings')  # adjust as needed

# Setup Django
django.setup()

# Get environment variables from .env file
BACKBLAZE_ENDPOINT = os.getenv("B2_ENDPOINT")
BACKBLAZE_KEY_ID = os.getenv("B2_ACCESS_KEY")
BACKBLAZE_APPLICATION_KEY = os.getenv("B2_SECRET_KEY")
BACKBLAZE_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")

# Set the media directory from Django settings (adjust as needed)
MEDIA_ROOT = settings.MEDIA_ROOT

# Initialize a boto3 client for Backblaze B2
def get_b2_client():
    return boto3.client(
        's3',
        endpoint_url=BACKBLAZE_ENDPOINT,
        aws_access_key_id=BACKBLAZE_KEY_ID,
        aws_secret_access_key=BACKBLAZE_APPLICATION_KEY
    )

# Upload a single file to the Backblaze bucket
def upload_file_to_b2(file_path, file_name):
    b2_client = get_b2_client()
    try:
        # Upload the file to the Backblaze B2 bucket
        b2_client.upload_file(file_path, BACKBLAZE_BUCKET_NAME, file_name)
        print(f"Uploaded {file_name} to {BACKBLAZE_BUCKET_NAME}")
    except ClientError as e:
        print(f"Error uploading {file_name}: {e}")

# Upload all media files in MEDIA_ROOT to Backblaze
def upload_all_media_files():
    # Iterate over all files in the MEDIA_ROOT directory
    for root, dirs, files in os.walk(MEDIA_ROOT):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Relative path in the media folder
            relative_file_path = os.path.relpath(file_path, MEDIA_ROOT).replace("\\", "/")
            # Upload each file
            upload_file_to_b2(file_path, relative_file_path)

upload_all_media_files()