from django.urls import path, include
from rest_framework.routers import SimpleRouter
from fauna import views

router = SimpleRouter()
router.register("animals", viewset=views.AnimalViewSet, basename="animals")

urlpatterns = [
    path('', include(router.urls))]
