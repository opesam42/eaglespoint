from django.db import models
from listing.models import Listings

# Create your models here.

class ContactMessage(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=20)
    sender_email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    # if the user is enquiring for a specific property
    property = models.ForeignKey(Listings, on_delete=models.SET_NULL, blank=True, null=True, related_name='contact_messages')

    def __str__(self):
        return f"{self.subject} from {self.sender_name}"