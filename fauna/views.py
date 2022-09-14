from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from fauna.models import Animal
from fauna.serializers import AnimalSerializer


class AnimalsView(ReadOnlyModelViewSet):
    queryset = Animal.objects.all()

    serializer_class = AnimalSerializer
    permission_classes = (AllowAny,)