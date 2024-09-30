from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, GoogleLoginView

# Router for user-related actions (including the 'me' endpoint)
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    # Auth-related JWT Endpoints (auth operations)
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),

    # User profile endpoint for the authenticated user ('me' actions)
    path('auth/me/', CustomUserViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me'}), name='me'),
    path('auth/users/', CustomUserViewSet.as_view({'get': 'reterive', 'post': 'create',"get":"list",}), name='users'),
    path('auth/users/<uuid:uuid>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',}), name='user'),
    path('auth/users/activation/', CustomUserViewSet.as_view({'post': 'activation'}), name='activation'),
    path('auth/users/resend_activation/', CustomUserViewSet.as_view({'post': 'resend_activation'}), name='resend_activation'),
    path('auth/users/reset_password/', CustomUserViewSet.as_view({'post': 'reset_password'}), name='reset_password'),
    path('auth/users/reset_password_confirm/', CustomUserViewSet.as_view({'post': 'reset_password_confirm'}), name='reset_password_confirm'),
    path('auth/users/set_password/', CustomUserViewSet.as_view({'post': 'set_password'}), name='set_password'),
    path('auth/social/google/', GoogleLoginView.as_view(),name='social'),
]
