from django.urls import path

from prediction import views

urlpatterns = [
    path('prediction', views.prediction, name='prediction'),
    path('', views.choix, name='choix'),
]