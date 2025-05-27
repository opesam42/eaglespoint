from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model
import re
from urllib.parse import urlparse
from utils.storage import BackBlazeAPI

User = get_user_model()

# Create your models here.
class BlogArticle(models.Model):

    ARTICLE_CATEGORY = (
        ('general', 'General'),
        ('travel', 'Travel'),
        ('real_estate', 'Real Estate')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=ARTICLE_CATEGORY, default='general')
    content = CKEditor5Field(config_name='extends')
    excerpt = models.TextField(max_length=500, blank=True, null=True)
    cover_image = models.ImageField(upload_to='blog/cover-images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)

    def _normalize_signed_media_urls(self):
        if self.content:
            pattern = r'https://s3\.eu-central-003\.backblazeb2\.com/eaglespoint-website/([^"?]+)\?[^"]+'
            self.content = re.sub(pattern, 'https://eaglespoint-website.s3.eu-central-003.backblazeb2.com/' + r'\1', self.content)

    def _delete_old_cover_image(self):
        if self.pk:
            old_instance = BlogArticle.objects.get(pk=self.pk)
            if old_instance.cover_image and old_instance.cover_image != self.cover_image:
                try:
                    backblaze = BackBlazeAPI()
                    backblaze.delete_files_with_prefix(old_instance.cover_image.name)
                    print("Cover image", old_instance.cover_image.name)
                except Exception as e:
                    print(f'Backblaze error: {e}')

    
    def _get_image_urls(self, html_content):
        """Extract image URLs from rich text (HTML)."""
        return re.findall(r'<img[^>]+src="([^">]+)"', html_content or '')
    
    
    def _get_image_paths(self, urls):
        """
        Get relative file paths from full S3/local URLs for deletion.
        Adjust this depending on your storage setup.
        """
        paths = []
        bucket_name = 'eaglespoint-website'
        for url in urls:
            parsed_url = urlparse(url)
            if 'eaglespoint-website' in url:
                path = parsed_url.path.lstrip('/')
                if path.startswith(f'{bucket_name}/'):
                    path = path[len(f'{bucket_name}/'):]  # Remove 'eaglespoint-website/'
                paths.append(path)
        return paths
    
    def _compare_and_delete_images(self):
        if self.pk:
            old_content = BlogArticle.objects.get(pk=self.pk).content
            new_content = self.content

            old_image_urls = set(self._get_image_urls(old_content))
            new_image_urls = set(self._get_image_urls(new_content))

            removed_image_urls = old_image_urls - new_image_urls
            removed_image_paths = self._get_image_paths(removed_image_urls)
            print("Remove Image URL", removed_image_paths)

            for path in removed_image_paths:
                try:
                    backblaze = BackBlazeAPI()
                    backblaze.delete_files_with_prefix(path)
                    print("Deleted multiple image:", path)
                except Exception as e:
                    print(f'Backblaze error: {e}')
    

    def save(self, *args, **kwargs):
        self._delete_old_cover_image()
        self._compare_and_delete_images()

        if not self.slug:
            base_slug = slugify(self.title)[:180]
            slug = base_slug
            counter = 1
            # Ensure slug uniqueness
            while BlogArticle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    
    def _delete_all_images(self):
        # delete cover image
        if self.cover_image:
            try:
                backblaze = BackBlazeAPI()
                backblaze.delete_files_with_prefix(self.cover_image.name)
            except Exception as e:
                print(f'Backblaze error: {e}')

        #delete inline images
        content = self.content or ""
        image_urls = set(self._get_image_urls(content))
        image_paths = self._get_image_paths(image_urls)
        print(image_paths)

        for path in image_paths:
            try:
                backblaze = BackBlazeAPI()
                backblaze.delete_files_with_prefix(path)
                print("Deleted multiple image:", path)
            except Exception as e:
                print(f'Backblaze error: {e}')
        

    def delete(self, *args, **kwargs):
        self._delete_all_images()

        super().delete(*args, **kwargs)


    def __str__(self):
        return f'{self.title}'