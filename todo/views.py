from rest_framework.permissions import IsAuthenticated
from .serializers import TodoSerializer
from .models import Todo
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, extend_schema

# Make the schema view of the ToDo app
@extend_schema_view(
    list=extend_schema(
        summary="List all ToDos",
        description="Retrieve a list of all ToDo items.",
        tags=["ToDo"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a ToDo",
        description="Retrieve a specific ToDo item by its ID.",
        tags=["ToDo"],
    ),
    create=extend_schema(
        summary="Create a new ToDo",
        description="Create a new ToDo item. The authenticated user will automatically be assigned as the owner.",
        tags=["ToDo"],
    ),
    update=extend_schema(
        summary="Update an existing ToDo",
        description="Update an existing ToDo item by its ID.",
        tags=["ToDo"],
    ),
    partial_update=extend_schema(
        summary="Partially update a ToDo",
        description="Partially update an existing ToDo item.",
        tags=["ToDo"],
    ),
    destroy=extend_schema(
        summary="Delete a ToDo",
        description="Delete a specific ToDo item by its ID.",
        tags=["ToDo"],
    ),
)
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user to the authenticated user
        serializer.save(user=self.request.user)
