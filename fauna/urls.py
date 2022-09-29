from django.urls import include, path
from rest_framework.routers import SimpleRouter

from fauna import views

router = SimpleRouter()
router.register(r'animals', views.AnimalViewSet, basename='animals')

urlpatterns = [
    path('', include(router.urls))
]
