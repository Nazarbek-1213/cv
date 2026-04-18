from django.contrib import admin
from django.urls import path, include

from configapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='index.html'),
]

