from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet as DjoserUserViewSet
from .serializers import CustomUserCreateSerializer
from .models import CustomUser
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["me"],
    summary="Get the current user's info"
    )
@action(
    methods=['get', 'put', 'patch', 'delete'],
    detail=False,
    permission_classes=[permissions.IsAuthenticated]
    )
class CustomUserViewSet(DjoserUserViewSet):
    """
    Custom UserViewSet to handle both user registration and the 'me' endpoint separately.
    """

    serializer_class = CustomUserCreateSerializer
    queryset = CustomUser.objects.all()

    # Custom endpoint for 'me'
    
    def me(self, request, *args, **kwargs):
        """
        Overriding the default 'me' action to return the user's details.
        """
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    # Register endpoint (POST /auth/users/)
   # @extend_schema(request=CustomUserCreateSerializer, responses=CustomUserCreateSerializer)
   # def create(self, request, *args, **kwargs):
     #   return super().create(request, *args, **kwargs)
