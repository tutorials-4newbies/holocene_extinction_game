import copy

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import Length
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
# Create your views here.
from fauna.models import Animal
from fauna.permissions import IsCreatorMutatingOrReadOnly, LikePermission
from fauna.serializers import AnimalSerializer, AnonymousUserAnimalSerializer, UsersViewSerializer
from rest_framework.decorators import action


class AnimalViewSet(ModelViewSet):
    queryset = Animal.objects.all()
    permission_classes = [IsCreatorMutatingOrReadOnly]
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

    def create(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data["creator"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["POST"], detail=True, permission_classes=[LikePermission])
    def like(self, request, pk=None):
        """
        /animals/pk(1)/like
        """
        # get the animal
        animal: Animal = self.get_object()
        animal.likes.add(request.user)
        # add a like and save
        # return the animal
        serializer = self.get_serializer(animal)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(methods=["GET"], detail=False)
    def dashboard(self, requset):
        animals = Animal.objects.annotate(
            likes_counter=Count("likes"),
            nameLength=Length("name")
        )\
            .all().order_by("-likes_counter")
        serializer = self.get_serializer(animals, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UsersView(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    serializer_class = UsersViewSerializer
