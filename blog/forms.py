from django import forms
from .models import BlogArticle
from django_ckeditor_5.widgets import CKEditor5Widget

class BlogArticleForm(forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = ['title', 'category', 'content', 'excerpt', 'cover_image', 'published', 'tags']
        
        widgets = {
            'content': CKEditor5Widget(config_name='default')
        }