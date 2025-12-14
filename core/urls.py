from django.urls import path
from .views import home_api

urlpatterns = [
    path('api/', home_api, name='home_api'),
]