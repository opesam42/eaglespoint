import boto3
from django.conf import settings
import os

access_key = os.getenv('B2_ACCESS_KEY')
secret_key = os.getenv('B2_SECRET_KEY')
bucket_name = os.getenv('B2_BUCKET_NAME')
region_name = B2_REGION = os.getenv('B2_REGION')
endpoint_url = os.getenv('B2_ENDPOINT')

class B2UploadAdapter:
    def __init__(self, loader):
        self.loader = loader

    def upload(self):
        # Get the file from CKEditor
        uploaded_file = self.loader.file
        
        # Initialize Backblaze B2 client
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        # Define file path and name
        file_name = f"uploads/{uploaded_file.name}"
        bucket_name = bucket_name

        # Upload file to Backblaze B2
        s3_client.upload_fileobj(
            uploaded_file,
            bucket_name,
            file_name,
            ExtraArgs={'ContentType': uploaded_file.content_type}
        )

        # Return the unsigned URL
        unsigned_url = f"{endpoint_url}/{bucket_name}/{file_name}"
        return {'url': unsigned_url}

    def abort(self):
        pass