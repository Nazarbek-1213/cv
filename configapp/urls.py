from django.urls import path

from configapp.views import home

urlpatterns = [
    path('', home, name='index.html'),
]
