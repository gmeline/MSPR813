from django import forms
import pandas as pd

class ElectionFilterForm(forms.Form):
    # Filtrer par départements
    df = pd.read_csv('core/data/leg_1993.csv', sep=',')
    departements = df['libelle_du_departement'].unique()
    department_choices = [(dep, dep) for dep in departements]
    department_field = forms.ChoiceField(
        choices=[('', 'Sélectionner un département')] + department_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    show_code_du_departement = forms.BooleanField(required=False, initial=False)
    show_libelle_du_departement = forms.BooleanField(required=False, initial=True)
    show_code_de_la_circonscription = forms.BooleanField(required=False, initial=True)
    show_inscrits = forms.BooleanField(required=False, initial=True)
    show_volants = forms.BooleanField(required=False, initial=True)
    show_exprimees = forms.BooleanField(required=False, initial=True)
    show_blancs_et_nuls = forms.BooleanField(required=False, initial=True)
    show_nuance = forms.BooleanField(required=False, initial=True)
    show_voix = forms.BooleanField(required=False, initial=True)
    show_nuance_2 = forms.BooleanField(required=False, initial=True)
    show_voix_2 = forms.BooleanField(required=False, initial=True)
    show_nuance_3 = forms.BooleanField(required=False, initial=True)
    show_voix_3 = forms.BooleanField(required=False, initial=True)
    show_annee = forms.BooleanField(required=False, initial=True)

    show_gagnant = forms.BooleanField(required=False, initial=True)
    show_voix_gagnant = forms.BooleanField(required=False, initial=True)
    show_gagnant_precedent = forms.BooleanField(required=False, initial=True)
    show_voix_gagnant_precedent = forms.BooleanField(required=False, initial=True)

    show_encodage_sans_centre_gagnant = forms.BooleanField(required=False, initial=True)
    show_encodage_avec_centre_gagnant = forms.BooleanField(required=False, initial=True)
    show_encodage_centre_extremes_gagnant = forms.BooleanField(required=False, initial=True)
    show_encodage_sans_centre_gagnant_precedent = forms.BooleanField(required=False, initial=True)
    show_encodage_avec_centre_gagnant_precedent = forms.BooleanField(required=False, initial=True)
    show_encodage_centre_extremes_gagnant_precedent = forms.BooleanField(required=False, initial=True)

    show_instabilite_sans_centre = forms.BooleanField(required=False, initial=True)
    show_poids_nuance_sans_centre = forms.BooleanField(required=False, initial=True)
    show_desir_changement_sans_centre = forms.BooleanField(required=False, initial=True)

    show_instabilite_avec_centre = forms.BooleanField(required=False, initial=True)
    show_poids_nuance_avec_centre = forms.BooleanField(required=False, initial=True)
    show_desir_changement_avec_centre = forms.BooleanField(required=False, initial=True)

    show_instabilite_centre_extremes = forms.BooleanField(required=False, initial=True)
    show_poids_nuance_centre_extremes = forms.BooleanField(required=False, initial=True)
    show_desir_changement_centre_extremes = forms.BooleanField(required=False, initial=True)

class ImportCSVForm(forms.Form):
    csv_file = forms.FileField()
