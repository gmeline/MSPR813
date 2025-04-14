from django.urls import path

from dashboard.urls import urlpatterns
from exploration import views

urlpatterns =  [
    path('', views.index, name='exploration'),
]