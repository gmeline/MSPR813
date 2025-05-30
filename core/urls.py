from django.urls import path
from . import views
from .views import GeneratedImageListView

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('recherche/', views.recherche, name='recherche'),
    path('create/category/', views.creation_categorie, name='creation_categorie'),
    path('create/article/', views.creation_article, name='creation_article'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('images/', GeneratedImageListView, name='generated_image_list'),
    path('graphique/', views.render_graphique_page, name='graphique'),
    path('list-buckets/', views.list_gcs_buckets, name='list-buckets'),
]
