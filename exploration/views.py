from django.shortcuts import render
from .forms import ElectionFilterForm
from .models import ResultatElection
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.db import models
import pandas as pd


def index(request):
    csv_path = os.path.join(settings.BASE_DIR, 'exploration', 'data', 'leg_1993.csv')
    
    if not os.path.exists(csv_path):
        return render(request, 'exploration/index.html', {
            'error': 'Le fichier CSV est introuvable.',
        })
    
    df = pd.read_csv(csv_path, sep=',')
    departements = df['libelle_du_departement'].unique()
    nuances = df['nuance'].unique()
    form = ElectionFilterForm(request.GET)

    if form.is_valid():
        selected_department = form.cleaned_data.get('department_field')
        selected_nuance = form.cleaned_data.get('nuance_field')

        if selected_department:
            df = df[df['libelle_du_departement'] == selected_department]
        
        if selected_nuance:
            df = df[df['nuance'] == selected_nuance]

        show_code_du_departement = form.cleaned_data.get('show_code_du_departement')
        show_libelle_du_departement = form.cleaned_data.get('show_libelle_du_departement')
        show_code_de_la_circonscription = form.cleaned_data.get('show_code_de_la_circonscription')
        show_inscrits = form.cleaned_data.get('show_inscrits')
        show_volants = form.cleaned_data.get('show_volants')
        show_exprimees = form.cleaned_data.get('show_exprimees')
        show_blancs_et_nuls = form.cleaned_data.get('show_blancs_et_nuls')
        show_nuance = form.cleaned_data.get('show_nuance')
        show_voix = form.cleaned_data.get('show_voix')
        show_nuance_2 = form.cleaned_data.get('show_nuance_2')
        show_voix_2 = form.cleaned_data.get('show_voix_2')
        show_nuance_3 = form.cleaned_data.get('show_nuance_3')
        show_voix_3 = form.cleaned_data.get('show_voix_3')
        show_annee = form.cleaned_data.get('show_annee')
        show_gagnant = form.cleaned_data.get('show_gagnant')
        show_voix_gagnant = form.cleaned_data.get('show_voix_gagnant')
        show_gagnant_precedent = form.cleaned_data.get('show_gagnant_precedent')
        show_voix_gagnant_precedent = form.cleaned_data.get('show_voix_gagnant_precedent')
        show_encodage_sans_centre_gagnant = form.cleaned_data.get('show_encodage_sans_centre_gagnant')
        show_encodage_avec_centre_gagnant = form.cleaned_data.get('show_encodage_avec_centre_gagnant')
        show_encodage_centre_extremes_gagnant = form.cleaned_data.get('show_encodage_centre_extremes_gagnant')
        show_encodage_sans_centre_gagnant_precedent = form.cleaned_data.get('show_encodage_sans_centre_gagnant_precedent')
        show_encodage_avec_centre_gagnant_precedent = form.cleaned_data.get('show_encodage_avec_centre_gagnant_precedent')
        show_encodage_centre_extremes_gagnant_precedent = form.cleaned_data.get('show_encodage_centre_extremes_gagnant_precedent')
        show_instabilite_sans_centre = form.cleaned_data.get('show_instabilite_sans_centre')
        show_poids_nuance_sans_centre = form.cleaned_data.get('show_poids_nuance_sans_centre')
        show_desir_changement_sans_centre = form.cleaned_data.get('show_desir_changement_sans_centre')
        show_instabilite_avec_centre = form.cleaned_data.get('show_instabilite_avec_centre')
        show_poids_nuance_avec_centre = form.cleaned_data.get('show_poids_nuance_avec_centre')
        show_desir_changement_avec_centre = form.cleaned_data.get('show_desir_changement_avec_centre')
        show_instabilite_centre_extremes = form.cleaned_data.get('show_instabilite_centre_extremes')
        show_poids_nuance_centre_extremes = form.cleaned_data.get('show_poids_nuance_centre_extremes')
        show_desir_changement_centre_extremes = form.cleaned_data.get('show_desir_changement_centre_extremes')

    data = df.values.tolist() if not df.empty else []

    if not df.empty:
        if 'voix' not in df.columns:
            return render(request, 'exploration/index.html', {
                'error': 'La colonne "voix" est manquante dans le fichier CSV.',
            })
        
        df['voix'] = pd.to_numeric(df['voix'], errors='coerce')
        df = df.dropna(subset=['voix'])
        return render(request, 'exploration/index.html', {
            'form': form,
            'data': data,
            'show_code_du_departement': show_code_du_departement,
            'show_libelle_du_departement': show_libelle_du_departement,
            'show_code_de_la_circonscription': show_code_de_la_circonscription,
            'show_inscrits': show_inscrits,
            'show_volants': show_volants,
            'show_exprimees': show_exprimees,
            'show_blancs_et_nuls': show_blancs_et_nuls,
            'show_nuance': show_nuance,
            'show_voix': show_voix,
            'show_nuance_2': show_nuance_2,
            'show_voix_2': show_voix_2,
            'show_nuance_3': show_nuance_3,
            'show_voix_3': show_voix_3,
            'show_annee': show_annee,
            'show_gagnant': show_gagnant,
            'show_voix_gagnant': show_voix_gagnant,
            'show_gagnant_precedent': show_gagnant_precedent,
            'show_voix_gagnant_precedent': show_voix_gagnant_precedent,
            'show_encodage_sans_centre_gagnant': show_encodage_sans_centre_gagnant,
            'show_encodage_avec_centre_gagnant': show_encodage_avec_centre_gagnant,
            'show_encodage_centre_extremes_gagnant': show_encodage_centre_extremes_gagnant,
            'show_encodage_sans_centre_gagnant_precedent': show_encodage_sans_centre_gagnant_precedent,
            'show_encodage_avec_centre_gagnant_precedent': show_encodage_avec_centre_gagnant_precedent,
            'show_encodage_centre_extremes_gagnant_precedent': show_encodage_centre_extremes_gagnant_precedent,
            'show_instabilite_sans_centre': show_instabilite_sans_centre,
            'show_poids_nuance_sans_centre': show_poids_nuance_sans_centre,
            'show_desir_changement_sans_centre': show_desir_changement_sans_centre,
            'show_instabilite_avec_centre': show_instabilite_avec_centre,
            'show_poids_nuance_avec_centre': show_poids_nuance_avec_centre,
            'show_desir_changement_avec_centre': show_desir_changement_avec_centre,
            'show_instabilite_centre_extremes': show_instabilite_centre_extremes,
            'show_poids_nuance_centre_extremes': show_poids_nuance_centre_extremes,
            'show_desir_changement_centre_extremes': show_desir_changement_centre_extremes,
            'departements': departements,
            'nuances': nuances,
            'graph_image_url': '/static/images/tableau.png',
        })

    return render(request, 'exploration/index.html', {
        'form': form,
        'data': data,
        'departements': departements,
        'nuances': nuances,
    })
