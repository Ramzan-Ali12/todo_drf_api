# users/urls.py

from django.urls import path
from .views import CustomUserViewSet

urlpatterns = [
    path('me/', CustomUserViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me','delete': 'me'}), name='user-me'),     
    ]
