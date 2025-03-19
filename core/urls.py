from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'), 
    path('recherche/', views.recherche, name='recherche'), 
    path('create/category/', views.creation_categorie, name='creation_categorie'),
    path('create/article/', views.creation_article, name='creation_article'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),  
]
