from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Article, GeneratedImage
from .forms import CategoryForm, ElectionFilterForm, ArticleForm
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import os
from django.conf import settings

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

def render_graphique_page(request):

    df = pd.read_csv('/Users/gmeline/Documents/EPSI_24-26/24-25/MSPR/appMSPR/core/data/graphique_data.csv')

    print("Colonnes disponibles dans le CSV:", df.columns)

    dates_uniques = sorted(df['Date'].unique())  

    date_field = request.GET.get('date_field')

    if date_field:
        df = df[df['Date'] == date_field]

    data = df.values.tolist()  

    if not df.empty:
        df['Pourcentage'] = df['Pourcentage'].str.replace('%', '').astype(float)

        candidats = df['Candidat'].unique() 
        pourcentages = df.groupby('Candidat')['Pourcentage'].sum() 

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(pourcentages.index, pourcentages.values)

        ax.set_xlabel('Candidats')
        ax.set_ylabel('Pourcentage')
        ax.set_title('Pourcentage des candidats')

        plt.xticks(rotation=90)

        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'graphique.png')

        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        fig.savefig(image_path)

        plt.close(fig)

        return render(request, 'core/graphique.html', {
            'dates': dates_uniques,
            'selected_date': date_field,
            'data': data,
            'graph_image_url': '/static/images/graphique.png', 
        })

   
    return render(request, 'core/graphique.html', {
        'dates': dates_uniques,
        'selected_date': date_field,
        'data': data,
    })

def election_filter_view(request):
    form = ElectionFilterForm(request.GET) 

    articles_filtered = [] 

    if form.is_valid():
        election_date = form.cleaned_data.get('election_date')
        if election_date:
            articles_filtered = Article.objects.filter(date__exact=election_date)
    
    return render(request, 'core/graphique.html', {
        'form': form,
        'articles': articles_filtered,
    })
