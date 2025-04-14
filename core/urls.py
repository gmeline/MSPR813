from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('recherche/', views.recherche, name='recherche'),
    path('create/category/', views.creation_categorie, name='creation_categorie'),
    path('create/article/', views.creation_article, name='creation_article'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('tableau/', views.tableau_page, name='tableau'),
    path('list-buckets/', views.list_gcs_buckets, name='list-buckets'),
    path('data-request/', views.dataRequest, name='data_request'),
    path('csv/', views.lire_csv, name='lire_csv'),
    path('election_results/', views.election_results, name='election_results'),
    path('import_csv/', views.import_csv, name='import_csv'),
]
