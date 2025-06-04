from django import forms
from .models import Testimonial, FAQ, TeamMember, Partners

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'category', 'message', 'is_active']

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'photo', 'position']

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partners
        fields = ['name', 'logo']