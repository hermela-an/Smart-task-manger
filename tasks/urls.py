from django.urls import path
from .views import (TaskListCreateView, TaskDetailView, TaskStatisticsView,TaskDueDateReminderView )

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/statistics/', TaskStatisticsView.as_view(), name='task-statistics'),
    path('tasks/reminders/', TaskDueDateReminderView.as_view(), name='task-reminders'),
]