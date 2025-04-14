from b2sdk.v1 import InMemoryAccountInfo, B2Api
import os

bucket_name = os.getenv('B2_BUCKET_NAME')

def get_signed_b2_url(file_name, bucket_name=bucket_name, duration_in_seconds=3600):
    """
    Generate a signed URL for a private Backblaze B2 file.
    """
    application_key_id = os.getenv('B2_ACCESS_KEY')  # or replace with actual key
    application_key = os.getenv('B2_SECRET_KEY')  # or replace with actual key

    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", application_key_id, application_key)

    bucket = b2_api.get_bucket_by_name(bucket_name)
    download_url = bucket.get_download_url(file_name)
    # download_url = bucket.get_download_url_by_name(file_name, duration_in_seconds)
    return download_url
