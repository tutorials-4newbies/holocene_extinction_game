from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.
from fauna.models import Animal
from fauna.serializers import AnimalSerializer, AnonymousUserAnimalSerializer


class AnimalViewSet(ReadOnlyModelViewSet):
    queryset = Animal.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AnonymousUserAnimalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['period', 'extinction']

    # Override get_serialzier_class to choose by class by request.user.is_authenticated
    def get_serializer_class(self):
        serializer_class = super(AnimalViewSet, self).get_serializer_class()
        if self.request.user.is_authenticated:
            serializer_class = AnimalSerializer
        return serializer_class