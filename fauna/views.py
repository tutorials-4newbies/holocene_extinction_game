from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
# Create your views here.
from fauna.models import Animal
from fauna.serializers import AnimalSerializer, AnonymousUserAnimalSerializer


class AnimalViewSet(ModelViewSet):
    queryset = Animal.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AnonymousUserAnimalSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["period"]
    search_fields = ["name"]
    page_size = 100

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.request.user.is_authenticated:
            serializer_class = AnimalSerializer
        return serializer_class


