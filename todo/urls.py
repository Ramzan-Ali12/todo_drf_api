from django.urls import path
from .views import TodoViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

urlpatterns = [
  router.register("", TodoViewSet,basename="todo"),
]
urlpatterns = router.urls

