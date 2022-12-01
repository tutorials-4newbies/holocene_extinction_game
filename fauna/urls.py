from django.urls import path, include
from rest_framework.routers import SimpleRouter
from fauna import views

router = SimpleRouter()
router.register("animals", viewset=views.AnimalViewSet, basename="animals")
router.register("users", viewset=views.UsersView, basename="users")

urlpatterns = [
    path('', include(router.urls))]
