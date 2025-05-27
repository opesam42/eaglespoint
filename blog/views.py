from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import BlogArticle
from .forms import BlogArticleForm

# Create your views here.

def blog_create(request):
    form = BlogArticleForm(request.POST, request.FILES)
    categories = BlogArticle.ARTICLE_CATEGORY
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': "New blog article has been added"})
    return render(request, 'blog/create.html', {'form':form, 'categories': categories})

def view_all_blogs(request):
    blogs = BlogArticle.objects.all()
    return render(request, 'blog/index.html', {'blogs': blogs})

def view_specific_blog(request, slug):
    if slug:
        article = get_object_or_404(BlogArticle, slug=slug)
        return render(request, 'blog/article.html', {'article':article})