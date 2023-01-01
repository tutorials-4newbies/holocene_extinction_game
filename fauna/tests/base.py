import json
from typing import Dict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from fauna.models import Animal


def given_user_authenticated(client, username, password):
    auth_url = reverse("api-token-obtain-pair")
    res = client.post(auth_url, data=dict(username=username, password=password))
    access_token = res.data["access"]
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)


def given_user_unauthenticated(client):
    client.credentials(HTTP_AUTHORIZATION="")


def given_animal_exists(animal_params: Dict[str, str]) -> Animal:
    obj, created = Animal.objects.get_or_create(**animal_params)
    return obj


def given_user_exists(username, email, password, is_staff=False, is_superuser=False) -> User:
    obj = User.objects.create_user(username=username, email=email, password=password, is_staff=is_staff,
                                   is_superuser=is_superuser)
    return obj
