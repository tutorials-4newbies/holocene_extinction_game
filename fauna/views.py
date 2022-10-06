from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.
from fauna.models import Animal
from fauna.serializers import AnimalSerializer, AnonymosUsesrAnimalSerializer


class AnimalViewSet(ReadOnlyModelViewSet):
    queryset = Animal.objects.get_queryset().order_by('id')
    permission_classes = [AllowAny]
    serializer_class = AnonymosUsesrAnimalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["period"]
    search_fields = ["name"]

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.request.user.is_authenticated:
            serializer_class = AnimalSerializer
        return serializer_class

