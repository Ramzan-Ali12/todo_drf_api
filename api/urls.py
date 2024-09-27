from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from users.views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView

urlpatterns = [
    # Admin and schema-related URLs
    path("admin/", admin.site.urls),
    path('api/v1/auth/users/', include('users.urls')),
    path('docs/v1/', SpectacularAPIView.as_view(), name='openapi-schema') ,
    path('docs/', SpectacularSwaggerView.as_view(url_name='openapi-schema'), name='docs-ui'),
    # Auth Operation
    path("api/v1/auth/",include("djoser.urls")),
    # JWT-related endpoints under "api/v1/auth/jwt/"
    path('api/v1/auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/jwt/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/jwt/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),

    # Todo-related endpoints under "api/v1/todo/"
    path("api/v1/todo/", include("todo.urls")),
]
