from datetime import date, timedelta

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Task
from .serializers import TaskSerializer


# --------------------------------------------------
# List & Create Tasks (user-specific)
# --------------------------------------------------
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'priority']
    ordering_fields = ['due_date', 'created_at']
    search_fields = ['title']

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# --------------------------------------------------
# Retrieve, Update, Delete a Single Task
# --------------------------------------------------
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


# --------------------------------------------------
# D3-A: Task Statistics
# --------------------------------------------------
class TaskStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_tasks = Task.objects.filter(owner=user).count()
        completed_tasks = Task.objects.filter(owner=user, status='completed').count()
        pending_tasks = Task.objects.filter(owner=user, status='pending').count()
        in_progress_tasks = Task.objects.filter(owner=user, status='in_progress').count()

        completion_percentage = 0
        if total_tasks > 0:
            completion_percentage = round((completed_tasks / total_tasks) * 100, 2)

        return Response({
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completion_percentage": completion_percentage
        })


# --------------------------------------------------
# D3-B: Due-Date Reminders (Smart Logic)
# --------------------------------------------------
class TaskDueDateReminderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = date.today()
        soon_limit = today + timedelta(days=7)

        overdue_tasks = Task.objects.filter(
            owner=user,
            due_date__lt=today,
            status__in=['pending', 'in_progress']
        )

        due_today_tasks = Task.objects.filter(
            owner=user,
            due_date=today,
            status__in=['pending', 'in_progress']
        )

        due_soon_tasks = Task.objects.filter(
            owner=user,
            due_date__gt=today,
            due_date__lte=soon_limit,
            status__in=['pending', 'in_progress']
        )

        return Response({
            "overdue": overdue_tasks.count(),
            "due_today": due_today_tasks.count(),
            "due_soon": due_soon_tasks.count()
        })