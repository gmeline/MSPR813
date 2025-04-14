from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Article, GeneratedImage
from .forms import CategoryForm, ElectionFilterForm, ArticleForm
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd
import os
from django.conf import settings
from django.http import HttpResponse
from google.cloud import bigquery
from .models import DataRequeteHTTP
from .models import ResultatElection
import csv


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



def tableau_page(request):
    csv_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'leg_1993.csv')
    
    if not os.path.exists(csv_path):
        return render(request, 'core/tableau.html', {
            'error': 'Le fichier CSV est introuvable.',
        })
    

    df = pd.read_csv(csv_path, sep=',')
    
    print("Colonnes disponibles dans le CSV:", df.columns)

    # Liste des départements uniques
    departements = df['libelle_du_departement'].unique()

    # Création du formulaire
    form = ElectionFilterForm(request.GET)

    if form.is_valid():
        # Récupérer les filtres
        selected_date = form.cleaned_data.get('date_field')
        selected_department = form.cleaned_data.get('department_field')

        # Filtrer les données par département
        if selected_department:
            df = df[df['libelle_du_departement'] == selected_department]

        # Filtrer les données par date si nécessaire
        if selected_date:
            df = df[df['annee'] == selected_date.year]

    # Liste vide pour les dates, car il n'y a pas de colonne 'Date'
    dates_uniques = []

    # Si df est vide, on définit 'data' comme une liste vide
    data = df.values.tolist() if not df.empty else []

    if not df.empty:
        # Vérifier si la colonne 'voix' existe
        if 'voix' not in df.columns:
            return render(request, 'core/tableau.html', {
                'error': 'La colonne "voix" est manquante dans le fichier CSV.',
            })
        
        # Nettoyage des voix pour s'assurer qu'elles sont bien sous forme numérique
        df['voix'] = pd.to_numeric(df['voix'], errors='coerce')

        # Vérifier si des valeurs ont été converties en NaN et les supprimer
        df = df.dropna(subset=['voix'])

        # Regrouper les données par nuance (candidat ou parti) et somme des voix
        voix_par_candidat = df.groupby('nuance')['voix'].sum().sort_values(ascending=False)

        # Rotation des labels pour une meilleure lisibilité
        plt.xticks(rotation=90)

        # Définir le chemin de l'image
        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'tableau.png')

        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Retourner la réponse avec les données et l'image du graphique
        return render(request, 'core/tableau.html', {
            'form': form,
            'dates': dates_uniques,  # Liste vide, puisque la colonne 'Date' n'existe pas
            'data': data,
            'graph_image_url': '/static/images/tableau.png', 
            'departements': departements  # Passer la liste des départements
        })

    # Si df est vide, retourner une réponse avec une liste vide pour 'data'
    return render(request, 'core/tableau.html', {
        'form': form,
        'dates': dates_uniques,  # Liste vide
        'data': data,
        'departements': departements  # Passer la liste des départements
    })


def election_filter_view(request):
    form = ElectionFilterForm(request.GET) 

    articles_filtered = [] 

    if form.is_valid():
        election_date = form.cleaned_data.get('election_date')
        if election_date:
            articles_filtered = Article.objects.filter(date__exact=election_date)
    
    return render(request, 'core/tableau.html', {
        'form': form,
        'articles': articles_filtered,
    })

def list_gcs_buckets(request):
    # Créer un client BigQuery avec un fichier de service
    client = bigquery.Client.from_service_account_json("core/mspr-454808-baf9c7d409e4.json")
    
    # Requête BigQuery
    query = """
        SELECT *
        FROM `mspr-454808.Legislative_DW.LEG_CIRC_T2_HDF_MERGE_DW`
    """
    query_job = client.query(query)  # Lancer la requête
    df = query_job.to_dataframe()    # Convertir le résultat en dataframe pandas
    
    df_html = df.head(50).to_html()  # Convertir les 5 premières lignes en HTML

    return HttpResponse(f"<h1>Résultats BigQuery :</h1>{df_html}")

def dataRequest(request):
    df = DataRequeteHTTP.RequetHTTP()
    
    if df.empty:
        return render(request, "core/test.html", {"error": "Erreur : Impossible de récupérer les données depuis BigQuery."})

    df_html = df.head(50).to_html()

    return render(request, "core/test.html", {"df_html": df_html})

def lire_csv(request):
    chemin_fichier = os.path.join(settings.BASE_DIR, 'core', 'data', 'leg_1993.csv')
    df = pd.read_csv(chemin_fichier)
    donnees = df.to_dict(orient='records')

    return render(request, 'core/tableau.html', {'donnees': donnees})

def election_results(request):
    results = ResultatElection.objects.all()
    return render(request, 'core/election_results.html', {'results': results})

def import_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]
        data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=";")
        
        # Skip header row
        next(data)

        for row in data:
            ResultatElection.objects.create(
                code_du_departement=row[0],
                libelle_du_departement=row[1],
                code_de_la_circonscription=row[2],
                inscrits=int(row[3]),
                votants=int(row[4]),
                exprimes=int(row[5]),
                blancs_et_nuls=int(row[6]),
                nuance=row[7],
                voix=int(row[8]),
                nuance_2=row[9] if row[9] else None,
                voix_2=int(row[10]) if row[10] else None,
                nuance_3=row[11] if row[11] else None,
                voix_3=int(row[12]) if row[12] else None,
                annee=int(row[13])
            )

    form = ImportCSVForm()
    return render(request, 'core/import_csv.html', {'form': form})