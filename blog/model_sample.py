from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = CKEditor5Field(config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if the object exists in the database (i.e., it's an update)
        if self.pk is not None:  # self.pk exists for saved objects
            # Update-specific logic here
            original = BlogPost.objects.get(pk=self.pk)  # Fetch the existing instance
            if original.body != self.body:
                self.body = f"<p>Updated: {self.body}</p>"  # Example: Add prefix to body
            print(f"Updating BlogPost ID {self.pk}: {self.title}")
        else:
            # Create-specific logic (optional)
            print(f"Creating new BlogPost: {self.title}")

        # Call the parent save method to save the instance
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    


from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = CKEditor5Field(config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Check if the object exists in the database (i.e., it's an update)
        if self.pk is not None:
            try:
                original = BlogPost.objects.get(pk=self.pk)  # Fetch existing instance
                # Update-specific validation or modification
                if original.body != self.body:
                    if '<script>' in self.body.lower():
                        raise ValidationError("Scripts are not allowed in updated content.")
                    self.body = f"<p>Updated: {self.body}</p>"  # Modify body for updates
                print(f"Validating update for BlogPost ID {self.pk}: {self.title}")
            except BlogPost.DoesNotExist:
                # Handle edge case where pk exists but object is not in DB
                raise ValidationError("BlogPost does not exist in the database.")
        else:
            # Create-specific validation (optional)
            if len(self.title) < 5:
                raise ValidationError("Title must be at least 5 characters for new posts.")
            print(f"Validating new BlogPost: {self.title}")

    def save(self, *args, **kwargs):
        # Run clean() before saving to ensure validation
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title