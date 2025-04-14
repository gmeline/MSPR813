from django.shortcuts import render
from .forms import ElectionFilterForm
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd
import os
from django.conf import settings

def index(request):
    csv_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'leg_1993.csv')
    
    if not os.path.exists(csv_path):
        return render(request, 'exploration/index.html', {
            'error': 'Le fichier CSV est introuvable.',
        })
    df = pd.read_csv(csv_path, sep=',')
    departements = df['libelle_du_departement'].unique()
    nuances = df['nuance'].unique()

    # Création du formulaire
    form = ElectionFilterForm(request.GET)

    if form.is_valid():
        # Récupérer les filtres
        selected_department = form.cleaned_data.get('department_field')
        selected_nuance = form.cleaned_data.get('nuance_field')

        # Filtrer les données par département
        if selected_department:
            df = df[df['libelle_du_departement'] == selected_department]
        if selected_nuance:
            df = df[df['nuance'] == selected_nuance]

    # Liste vide pour les dates, car il n'y a pas de colonne 'Date'
    dates_uniques = []

    # Si df est vide, on définit 'data' comme une liste vide
    data = df.values.tolist() if not df.empty else []

    if not df.empty:
        # Vérifier si la colonne 'voix' existe
        if 'voix' not in df.columns:
            return render(request, 'exploration/index.html', {
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
        return render(request, 'exploration/index.html', {
            'form': form,
            'dates': dates_uniques,  # Liste vide, puisque la colonne 'Date' n'existe pas
            'data': data,
            'graph_image_url': '/static/images/tableau.png', 
            'departements': departements,  # Passer la liste des départements
            'nuances': nuances
        })

    # Si df est vide, retourner une réponse avec une liste vide pour 'data'
    return render(request, 'exploration/index.html', {
        'form': form,
        'dates': dates_uniques,  # Liste vide
        'data': data,
        'departements': departements,  # Passer la liste des départements
        'naunces': nuances
    })