from django.test import TestCase
from utils.storage import BackBlazeAPI
# Create your tests here.

backblaze = BackBlazeAPI()

backblaze.delete_files_with_prefix('listing-images/listing_1/cover-image/secnodary-page-image.jpg')