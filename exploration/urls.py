from django.urls import path

from dashboard.urls import urlpatterns
from machineLearning import views

urlpatterns =  [
    path('', views.index, name='exploration'),
]