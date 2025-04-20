from django.urls import path

from dashboard import views

urlpatterns = [
    path('travail', views.travail, name='dashboard'),
    path('criminality', views.criminality, name='dashboard'),
    path('elections', views.elections, name='dashboard'),
]