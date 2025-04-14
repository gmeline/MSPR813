from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('machineLearning/', include('machineLearning.urls')),
    path('exploration/', include('exploration.urls')),
    path('core/', include('core.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
