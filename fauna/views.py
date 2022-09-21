from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.
from fauna.models import Animal
from fauna.serializers import AnimalSerializer


class AnimalViewSet(ReadOnlyModelViewSet):
    queryset = Animal.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AnimalSerializer
