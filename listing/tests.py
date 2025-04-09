import pymysql
from eaglespoint.settings import BASE_DIR, env
import os
from .models import ListingImages
from .models import Listings

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 

def move_files():

    for listing in Listings.objects.all():
        # print(listing.pk)
        listing_images = ListingImages.objects.filter(listing_id=listing)
        if listing_images:
            folder_path = f'{MEDIA_ROOT}/listing-images/listing_{listing.pk}/'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            for listing_image in listing_images:
                # print(listing_image.image)
                image_name = os.path.basename(listing_image.image.path)
                new_image_path = os.path.join(folder_path, image_name)
                print(new_image_path)
                # print(image)
                if( os.rename(listing_image.image.path, new_image_path) ):
                    print(f"{new_image_path} created successfully")
                
            
        else:
            print("No images!")

def change_file_path_in_db():
    for listing in Listings.objects.all():
        listing_images = ListingImages.objects.filter(listing_id=listing)
        if listing_images:
            folder_path = f'listing-images/listing_{listing.pk}/'
            for listing_image in listing_images:
                if 'listing_' not in listing_image.image.path:
                    image_name = os.path.basename(listing_image.image.path)
                    new_path = os.path.join(folder_path, image_name)
                    print(new_path)

                    listing_image.image.name = new_path
                    listing_image.save()


def transfer_cover_image():
    listings = Listings.objects.all()
    for listing in listings:
        print(listing.pk)
        folder_path = f'{MEDIA_ROOT}/listing-images/listing_{listing.pk}/cover-image'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        image_name = os.path.basename(listing.cover_image.path)
        new_image_path = os.path.join(folder_path, image_name)
        print(new_image_path)

        if( os.rename(listing.cover_image.path, new_image_path) ):
            print(f"{new_image_path} created successfully")
        
def change_file_path_in_db_cover_image():
    listings = Listings.objects.all()
    
    for listing in listings:
        # folder_path = f'listing-images/listing_{listing.pk}/cover-image/'
        image_name = os.path.basename(listing.cover_image.path)
        new_path = f'listing-images/listing_{listing.pk}/cover-image/{image_name}'
        print(new_path)
        print(f"Updating listing {listing.pk}: {new_path}")

        listing.cover_image = new_path
        listing.save()
