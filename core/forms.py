from django import forms
from .models import Category
from .models import Article
import pandas as pd

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent'] 

    parent = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True), 
        required=False,  
        empty_label="Aucune catégorie parente" 
    )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']

class ElectionFilterForm(forms.Form):
    # Récupérer les départements uniques dans le CSV
    df = pd.read_csv('core/data/leg_1993.csv', sep=',')
    departements = df['libelle_du_departement'].unique()
    department_choices = [(dep, dep) for dep in departements]
    department_field = forms.ChoiceField(
        choices=[('', 'Sélectionner un département')] + department_choices,
        required=False,  # Champ optionnel, ou tu peux le rendre obligatoire si nécessaire
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ImportCSVForm(forms.Form):
    csv_file = forms.FileField()
