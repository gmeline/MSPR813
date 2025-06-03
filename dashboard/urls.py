from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.travail, name='dashboard'),
    path('nuance-per-depertement', views.criminality, name='dashboard'),
]