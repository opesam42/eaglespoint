from django.db import models

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

    def __str__(self):
        return f"{self.name} - {self.position}"