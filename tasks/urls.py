from django.urls import path
from .views import task_list, task_detail

urlpatterns = [
    path('tasks/', task_list),              # List & Create
    path('tasks/<int:pk>/', task_detail),   # Retrieve, Update, Delete
]