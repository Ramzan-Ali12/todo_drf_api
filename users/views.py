from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet as DjoserUserViewSet
from .serializers import CustomUserCreateSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
class CustomUserViewSet(DjoserUserViewSet):
    """
    Custom UserViewSet to handle both user registration and the 'me' endpoint separately.
    """
    serializer_class = CustomUserCreateSerializer

    @extend_schema(
        tags=["me"],
        summary="GET the current authenticated user's profile",
        description="Endpoint to GET current authenticated user's profile",
        responses={
            200: OpenApiResponse(description="Successful Response with the authenticated user's profile")
        },
        methods=["GET"],
    )
    @extend_schema(
        tags=["me"],
        summary="Update the current authenticated user's profile",
        description="Endpoint to Update current authenticated user's profile full_name. NOTE: You need to provide email as well for this endpoint to work.",
          request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'full_name': {'type': 'string'},
                    'email': {'type': 'string', 'format': 'email'},
                },
                'required': ['email', 'full_name']
            }
        },
        responses={
            200: OpenApiResponse(description="Successful Response with the updated user's profile")
        },
        methods=["PUT"],
    )
    @extend_schema(
        tags=["me"],
        summary="Update the current authenticated user's profile",
        description="Endpoint to Update current authenticated user's profile full_name.",
          request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'full_name': {'type': 'string'},
                    'email': {'type': 'string', 'format': 'email'},
                },
                'required': ['email', 'full_name']
            }
        },
        responses={
            200: OpenApiResponse(description="Successful Response with the updated user's profile"),
            204: OpenApiResponse(description="Profile successfully deleted.")
        },
        methods=["PATCH"],
    )
    @action(
        methods=['get', 'put', 'patch'], 
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
        
@extend_schema(
    summary="generate access and refresh tokens for specific set of credentials",
    description="Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.",
    tags=["jwt"],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(
    summary="regenerate access token given valid refresh token",
    description="Takes a valid refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.",
    tags=["jwt"],
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(
    summary="verify access token is valid",
    description="Takes a token and indicates if it is valid. This view provides no information about a token's fitness for a particular use.",
    tags=["jwt"],
)
class CustomTokenVerifyView(TokenVerifyView):
    pass