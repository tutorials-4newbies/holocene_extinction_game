from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
# Create your views here.
from fauna.models import Animal
from fauna.serializers import AnimalSerializer


class AnimalViewSet(ReadOnlyModelViewSet):
    queryset = Animal.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AnimalSerializer

    # Add filters by django-filters rest framework integration or by overriding a queryset

    # Override get_serialzier_class to choose by class by request.user.is_authenticated