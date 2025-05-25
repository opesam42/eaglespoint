from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import BlogArticle

# Create your views here.

def view_all_blogs(request):
    blogs = BlogArticle.objects.all()
    return render(request, 'blog/index.html', {'blogs': blogs})

def view_specific_blog(request, slug):
    if slug:
        article = get_object_or_404(BlogArticle, slug=slug)
        return render(request, 'blog/article.html', {'article':article})