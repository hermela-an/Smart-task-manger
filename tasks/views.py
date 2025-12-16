from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  # type:ignore
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Task
from .serializers import TaskSerializer

# List & Create tasks (user-specific)
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'priority']      # Filtering
    ordering_fields = ['due_date', 'created_at']  # Ordering
    search_fields = ['title']                      # Searching

    def get_queryset(self):
        # Only return tasks owned by the logged-in user
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the task owner
        serializer.save(owner=self.request.user)


# Retrieve, Update, Delete a single task (user-specific)
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only the owner can access their tasks
        return Task.objects.filter(owner=self.request.user)