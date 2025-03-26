from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .models import Article
from .forms import CategoryForm
from .forms import ArticleForm
from .models import GeneratedImage

def accueil(request):
    return render(request, 'core/accueil.html')

def recherche(request):
    categories = Category.objects.filter(parent__isnull=True) 
    return render(request, 'core/recherche.html', {'categories': categories})

def creation_categorie(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('recherche')
    else:
        form = CategoryForm()
    
    return render(request, 'core/creation_categorie.html', {'form': form})

def creation_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('recherche') 
    else:
        form = ArticleForm()

    return render(request, 'core/creation_article.html', {'form': form})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Category.objects.filter(parent=category)
    articles = category.articles.all() 

    return render(request, 'core/category_detail.html', {
        'category': category,
        'subcategories': subcategories,
        'articles': articles
    })


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'core/article_detail.html', {'article': article})

def GeneratedImageListView(request):
    images = GeneratedImage.objects.all()
    return render(request, 'core/images_list.html', {'images': images})

