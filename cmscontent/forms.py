from django import forms
from .models import Testimonial, FAQ

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'category', 'message', 'is_active']