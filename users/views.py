from rest_framework import generics, permissions

from .serializers import CustomUserCreateSerializer
from .models import CustomUser
from drf_spectacular.utils import extend_schema


class CustomUserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to create an account

    @extend_schema(request=CustomUserCreateSerializer, responses=CustomUserCreateSerializer)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

