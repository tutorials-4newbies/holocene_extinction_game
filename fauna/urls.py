from rest_framework import routers
from django.urls import path, include

from fauna import views

router = routers.DefaultRouter()
router.register("animals", views.AnimalsView, basename="animals")

urlpatterns = [
    path('', include(router.urls))
]