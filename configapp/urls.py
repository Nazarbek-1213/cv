from django.urls import path

from configapp.views import home
from configapp.visit import visit

urlpatterns = [
    path('', home, name='index.html'),
    path('api/visit/', visit, name='api_visit'),
]
