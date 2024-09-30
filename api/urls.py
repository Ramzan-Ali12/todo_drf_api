from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin and schema-related URLs
    path("admin/", admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('docs/v1/', SpectacularAPIView.as_view(), name='openapi-schema') ,
    path('docs/', SpectacularSwaggerView.as_view(url_name='openapi-schema'), name='docs-ui'),    
    # Todo-related endpoints under "api/v1/todo/"
    path("api/v1/todo/", include("todo.urls")),
    
]
