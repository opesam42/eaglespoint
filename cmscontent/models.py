from django.db import models
from utils.storage import BackBlazeAPI

# Create your models here.
TESTIMONIAL_CATEGORIES = (
    ('real_estate', 'Real Estate'),
    ('travel', 'Travel')
)
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=TESTIMONIAL_CATEGORIES)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s Testimonial"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.question}"
    
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team_photos/')
    position = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)


    def _delete_old_photo(self):
        if self.pk:
            old_instance = TeamMember.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                try:
                    backblaze = BackBlazeAPI()
                    backblaze.delete_files_with_prefix(old_instance.photo.name)
                except Exception as e:
                    print(f'Backblaze error: {e}')


    def save(self, *args, **kwargs):
        self._delete_old_photo()
        if not self.pk:
            last_order = TeamMember.objects.aggregate(max_order=models.Max('order'))['max_order']
            self.order = (last_order or 0) + 1
        
        super().save(*args, **kwargs)


    def _delete_photo(self):
        # delete photo when team member is deleted
        if self.photo:
            try:
                backblaze = BackBlazeAPI()
                print(self.photo.name)
                backblaze.delete_files_with_prefix(self.photo.name)
            except Exception as e:
                print(f'Backblaze error: {e}')

    def delete(self, *args, **kwargs):
        self._delete_photo()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.position}"