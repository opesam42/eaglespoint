from django import forms
from .models import Testimonial, FAQ, TeamMember

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'category', 'message', 'is_active']

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'photo', 'position']