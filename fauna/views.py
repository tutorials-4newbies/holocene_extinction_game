from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from fauna.models import Animal
from fauna.serializers import AnimalSerializer


class AnimalViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AnimalSerializer
    permission_classes = [AllowAny]
    queryset = Animal.objects.all()
