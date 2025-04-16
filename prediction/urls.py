from django.urls import path

from prediction import views

urlpatterns = [
    path('', views.prediction, name='prediction'),
]