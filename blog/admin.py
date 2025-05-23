from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import BlogArticle
from django import forms

class BlogPostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditor5Widget(config_name='extends'))
    class Meta:
        model = BlogArticle
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm

admin.site.register(BlogArticle, BlogPostAdmin)