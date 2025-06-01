import dashboard
from django.urls import path

from prediction import views
from prediction.views import prediction

urlpatterns = [
    path('prediction_m1', views.prediction, name='prediction_m1'),
    path('prediction_m2', views.prediction, name='prediction_m2'),
    path('prediction_m3', views.prediction, name='prediction_m3'),
    path('', views.choix, name='choix'),
]