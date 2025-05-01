# views.py
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
    queryset = ResultatElection.objects.all()
    
    form = ElectionFilterForm(request.GET)
    
    departements = queryset.values_list('libelle_du_departement', flat=True).distinct()

    if form.is_valid():
        selected_department = form.cleaned_data.get('department_field')

        if selected_department:
            queryset = queryset.filter(libelle_du_departement=selected_department)

    columns_to_display = []
    if form.cleaned_data.get('show_code_du_departement'):
        columns_to_display.append('code_du_departement')
    if form.cleaned_data.get('show_libelle_du_departement'):
        columns_to_display.append('libelle_du_departement')
    if form.cleaned_data.get('show_code_de_la_circonscription'):
        columns_to_display.append('code_de_la_circonscription')
    if form.cleaned_data.get('show_inscrits'):
        columns_to_display.append('inscrits')
    if form.cleaned_data.get('show_votants'):
        columns_to_display.append('votants')
    if form.cleaned_data.get('show_exprimes'):
        columns_to_display.append('exprimes')
    if form.cleaned_data.get('show_blancs_et_nuls'):
        columns_to_display.append('blancs_et_nuls')
    if form.cleaned_data.get('show_nuance'):
        columns_to_display.append('nuance')
    if form.cleaned_data.get('show_voix'):
        columns_to_display.append('voix')
    if form.cleaned_data.get('show_nuance_2'):
        columns_to_display.append('nuance_2')
    if form.cleaned_data.get('show_nuance_3'):
        columns_to_display.append('nuance_3')
    if form.cleaned_data.get('show_voix_2'):
        columns_to_display.append('voix_2')
    if form.cleaned_data.get('show_voix_3'):
        columns_to_display.append('voix_3')
    if form.cleaned_data.get('show_annee'):
        columns_to_display.append('annee')
    if form.cleaned_data.get('show_gagnant'):
        columns_to_display.append('gagnant')
    if form.cleaned_data.get('show_voix_gagnant'):
        columns_to_display.append('voix_gagnant')
    if form.cleaned_data.get('show_gagnant_precedent'):
        columns_to_display.append('gagnant_precedent')
    if form.cleaned_data.get('show_voix_gagnant_precedent'):
        columns_to_display.append('voix_gagnant_precedent')
    if form.cleaned_data.get('show_encodage_sans_centre_gagnant'):
        columns_to_display.append('encodage_sans_centre_gagnant')
    if form.cleaned_data.get('show_encodage_avec_centre_gagnant'):
        columns_to_display.append('encodage_avec_centre_gagnant')
    if form.cleaned_data.get('show_encodage_centre_extremes_gagnant'):
        columns_to_display.append('encodage_centre_extremes_gagnant')
    if form.cleaned_data.get('show_encodage_sans_centre_gagnant_precedent'):
        columns_to_display.append('encodage_sans_centre_gagnant_precedent')
    if form.cleaned_data.get('show_encodage_avec_centre_gagnant_precedent'):
        columns_to_display.append('encodage_avec_centre_gagnant_precedent')
    if form.cleaned_data.get('show_encodage_centre_extremes_gagnant_precedent'):
        columns_to_display.append('encodage_centre_extremes_gagnant_precedent')

    if not columns_to_display:
        columns_to_display = [
            'code_du_departement', 'libelle_du_departement', 'code_de_la_circonscription',
            'inscrits', 'votants', 'exprimes', 'blancs_et_nuls', 'nuance', 'voix', 'nuance_2',
            'nuance_3', 'voix_2', 'voix_3', 'annee', 'gagnant', 'voix_gagnant', 'gagnant_precedent',
            'voix_gagnant_precedent', 'encodage_sans_centre_gagnant', 'encodage_avec_centre_gagnant',
            'encodage_centre_extremes_gagnant', 'encodage_sans_centre_gagnant_precedent',
            'encodage_avec_centre_gagnant_precedent', 'encodage_centre_extremes_gagnant_precedent'
        ]

    data = queryset.values(*columns_to_display)

    context = {
        'form': form,
        'data': list(data),
        'departements': departements,
    }

    return render(request, 'exploration/index.html', context)
