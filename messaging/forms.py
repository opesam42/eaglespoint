from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['sender_name', 'sender_phone', 'sender_email', 'subject', 'body', 'property']