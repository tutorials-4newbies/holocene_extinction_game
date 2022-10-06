from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.
from fauna.models import Animal
from fauna.serializers import AnimalSerializer, AnonymousAnimalSerializer


class AnimalViewSet(ReadOnlyModelViewSet):
    queryset = Animal.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AnonymousAnimalSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["period"]
    search_fields = ["name"]

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.request.user.is_authenticated:
            serializer_class = AnimalSerializer
        return serializer_class