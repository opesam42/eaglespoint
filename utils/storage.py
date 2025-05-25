import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from django.conf import settings
import os
from django.core.files.storage import default_storage
import requests
import json

B2_ENDPOINT = os.getenv('B2_ENDPOINT')
B2_ACCESS_KEY = os.getenv('B2_ACCESS_KEY')
B2_SECRET_KEY = os.getenv('B2_SECRET_KEY')
B2_REGION = os.getenv('B2_REGION')
B2_ENDPOINT = os.getenv('B2_ENDPOINT')
B2_BUCKET_NAME = os.getenv('B2_BUCKET_NAME')
BUCKET_ID = os.getenv('BUCKET_ID')

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

def append_image_prefix(image_url):
    return f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{image_url}'


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



class BackBlazeAPI:
    def __init__(self):
        self.access_key = B2_ACCESS_KEY
        self.secret_key = B2_SECRET_KEY
        self.bucket_id = BUCKET_ID
        self.authorize_account()
    

    def authorize_account(self):
        """ Authorize BackBlaze account """
        url = "https://api.backblazeb2.com/b2api/v3/b2_authorize_account"
        response = requests.get(url, auth=(self.access_key, self.secret_key))
        if response.status_code == 200:
            data = response.json()
            self.auth_token = data['authorizationToken']
            self.api_url = data['apiInfo']['storageApi']['apiUrl']
            self.download_url = data['apiInfo']['storageApi']['downloadUrl']
            self.account_id = data['accountId']
        else:
            raise Exception(f"Authorization failed: {response.status_code} - {response.text}")
    

    def delete_file(self, fileId, fileName):
        """ Delete file in Backblaze bucket """
        url = f'{self.api_url}/b2api/v3/b2_delete_file_version'
        headers = {"Authorization": self.auth_token}
        data = {
            'fileId': fileId,
            'fileName': fileName
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print(f"File '{fileName}' deleted successfully.")
        else:
            print(f"Failed to delete file '{fileName}': {response.status_code} {response.text}")


    def list_fileName_and_fileIds_with_prefix(self, prefix):
        """Return file id and file names of files fetched  """

        url = f'{self.api_url}/b2api/v3/b2_list_file_names'
        headers = {"Authorization": self.auth_token}
        data = {
            'bucketId': self.bucket_id,
            'prefix': prefix,
            'maxFileCount': 100
        }
        response = requests.post(url, headers=headers, json=data)
        all_files = []
        if response.status_code == 200:
            files_data = response.json()
            for file in files_data.get('files', []):
                all_files.append({
                    'fileId': file['fileId'],
                    'fileName': file['fileName']
                })
            return all_files

        else:
            raise Exception(f"List failed: {response.status_code} {response.text}")
        

    def delete_files_with_prefix(self, prefix):
        """ Takes in list of dictionary containing the id and name of the file for deletion """
        files = self.list_fileName_and_fileIds_with_prefix(prefix)
        
        for file in files:
            self.delete_file(file['fileId'], file['fileName'])
            print(f'Deleted {file['fileName']}')




from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class CustomS3Storage(S3Boto3Storage):
    access_key = os.getenv('B2_ACCESS_KEY')
    secret_key = os.getenv('B2_SECRET_KEY')
    bucket_name = os.getenv('B2_BUCKET_NAME')
    region_name = B2_REGION = os.getenv('B2_REGION')
    endpoint_url = os.getenv('B2_ENDPOINT')
    default_acl = None
    file_overwrite = False
    location = "uploads"  # Store files in the 'uploads' folder
