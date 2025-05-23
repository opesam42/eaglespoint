from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class BlogArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = CKEditor5Field(config_name='extends')
    excerpt = models.TextField(max_length=500, blank=True, null=True)
    cover_image = models.ImageField(upload_to='blog/cover-images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)

    def clean(self):
        pass

    def save(self, *args, **kwargs):
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

    def __str__(self):
        return f'{self.title}'