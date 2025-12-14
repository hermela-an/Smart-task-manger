from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

# List all tasks / Create a task (User-specific)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):
    if request.method == 'GET':
        # Only return tasks belonging to the logged-in user
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the owner to the logged-in user
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, Delete a single task (User-specific)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    try:
        # Only allow the owner to access their task
        task = Task.objects.get(pk=pk, owner=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = TaskSerializer(task, data=request.data, partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)