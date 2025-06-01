from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
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
    articles = BlogArticle.objects.filter(published=True).order_by('-created_at')
    travel_articles = articles.filter(category='travel')
    real_estate_articles = articles.filter(category='real_estate')
    general_articles = articles.filter(category='general')
    featured_articles = articles.filter(is_featured=True)
    hero_article = featured_articles.first() or articles.first()

    context = {
        'articles': articles,
        'real_estate_articles': real_estate_articles,
        'travel_articles': travel_articles,
        'general_articles': general_articles,
        'featured_articles': featured_articles,
        'hero_article':  hero_article,
    }
    return render(request, 'blog/index.html', context)


def search_blog(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        articles = BlogArticle.objects.all().order_by('-created_at')
    else:
        articles = BlogArticle.objects.filter(published=True).order_by('-created_at')

    selected_sort = request.GET.get('selected_sort', '')
    sort_options = {
        'date_desc': '-created_at',
        'date_asc': 'created_at',
    }

    order_by_field = sort_options.get(selected_sort, '-created_at') #default option '-created_at
    articles = articles.order_by(order_by_field)

    query = request.GET.get('query', '').strip() 
    if query:
        search_words = query.split() 

        queries = Q()
        for word in search_words:
            queries |=  Q(title__icontains=word) | Q(excerpt__icontains=word) | Q(tags__icontains=word)
        articles = articles.filter(queries)

    category = request.GET.get('category', '')
    published_status = request.GET.get('published_status', '')

    if category:
        articles = articles.filter(category = category)
    if published_status:
        articles = articles.filter(published=published_status)

    articles_count = articles.count()

    context = {
        'articles': articles,
        'articles_count':articles_count,
        'query': query,
    }

    #handle ajax request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'adminv2/blog/partials/blog-tables.html', context)

    
    return render(request, 'blog/search.html', context)


def view_specific_blog(request, slug=None, id=None):
    articles = BlogArticle.objects.all().order_by('-created_at')
    if slug:
        article = get_object_or_404(BlogArticle, slug=slug)
    else:
        article = get_object_or_404(BlogArticle, id=id)

    related_articles = article.get_related_posts(limit=4)

    context = {
        'article': article,
        'related_articles': related_articles,
        'articles': articles,
    }
    return render(request, 'blog/article.html', context)