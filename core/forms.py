from django import forms
from .models import Category
from .models import Article

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

