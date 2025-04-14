import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from django.conf import settings
import os
from django.core.files.storage import default_storage

B2_ENDPOINT = os.getenv('B2_ENDPOINT')
B2_ACCESS_KEY = os.getenv('B2_ACCESS_KEY')
B2_SECRET_KEY = os.getenv('B2_SECRET_KEY')
B2_REGION = os.getenv('B2_REGION')
B2_ENDPOINT = os.getenv('B2_ENDPOINT')
B2_BUCKET_NAME = os.getenv('B2_BUCKET_NAME')

def get_signed_b2_url(key, method='get_object'):
    s3 = boto3.client(
        's3',
        endpoint_url=B2_ENDPOINT,
        aws_access_key_id=B2_ACCESS_KEY,
        aws_secret_access_key=B2_SECRET_KEY,
        region_name=B2_REGION,
        config=Config(signature_version='s3v4'),
    )

    bucket_name = os.getenv('B2_BUCKET_NAME')
    params = {'Bucket': bucket_name, 'Key': key}

    try:
        url = s3.generate_presigned_url(
            method,
            Params=params,
            ExpiresIn=3600
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None


def delete_cover_image_folder(listing_id):
    s3 = boto3.client(
        's3',
        endpoint_url=B2_ENDPOINT,
        aws_access_key_id=B2_ACCESS_KEY,
        aws_secret_access_key=B2_SECRET_KEY,
    )

    folder_prefix = f'listing-images/listing_{listing_id}/cover-image/'

    try:
        # List objects in the folder
        response = s3.list_objects_v2(Bucket=B2_BUCKET_NAME, Prefix=folder_prefix)

        if 'Contents' not in response:
            print(f"No files found in folder: {folder_prefix}")
            return

        delete_list = [{'Key': obj['Key']} for obj in response['Contents']]

        # Print files being deleted (optional)
        for file in delete_list:
            print("Deleting:", file['Key'])

        # Delete all files (max 1000 per call)
        s3.delete_objects(
            Bucket=B2_BUCKET_NAME,
            Delete={'Objects': delete_list}
        )

        print(f"Deleted {len(delete_list)} file(s) in: {folder_prefix}")

    except ClientError as e:
        print(f"Error deleting files from {folder_prefix}: {e}")


def delete_cover_ima1ge_folder(listing_id):
    folder_path = f'listing-images/listing_{listing_id}/cover-image/'

    try:
        # List all files (second item in tuple)
        _, files = default_storage.listdir(folder_path)
        print(files)

        if not files:
            print(f"No files to delete in folder: {folder_path}")
            return

        for file_name in files:
            full_path = folder_path + file_name
            print("Deleting:", full_path)
            default_storage.delete(full_path)

        print(f"Deleted all files in folder: {folder_path}")

    except Exception as e:
        print(f"Error deleting files in {folder_path}: {str(e)}")