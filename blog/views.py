from django.shortcuts import render
from .models import BlogArticle

# Create your views here.

def view_all_blogs(request):
    blogs = BlogArticle.objects.all()
    return render(request, 'blog/index.html', {'blogs': blogs})