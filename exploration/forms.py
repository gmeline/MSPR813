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
    # Filtrer par nuance
    nuances=df['nuance'].unique()
    nuance_choices = [(nuan, nuan) for nuan in nuances]
    nuance_field = forms.ChoiceField(
        choices=[('', 'Sélectionner une nuance')] + nuance_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ImportCSVForm(forms.Form):
    csv_file = forms.FileField()
