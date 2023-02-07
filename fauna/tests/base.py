import json
from typing import Dict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fauna.models import Animal


class BaseTestCase(APITestCase):

    def setUp(self) -> None:
        self.admin_user = self.given_user_exists(username="admin_user",
                                                 email="admin@example.com",
                                                 password="12345",
                                                 is_staff=True,
                                                 is_superuser=True)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def when_authenticated_user_creates_animal_via_api(self, **animal_params):
        target_url = reverse("animals-list")
        animal = dict(period=animal_params.get("period", Animal.PERIOD_CHOICES[5][0]),
                      extinction=animal_params.get("extinction", "K/t"),
                      name=animal_params.get("name", "T-rex"),
                      taxonomy_class=animal_params.get("taxonomy_class", "Dinsourses"),
                      taxonomy_order=animal_params.get("taxonomy_order", "Thripods"),
                      taxonomy_family=animal_params.get("taxonomy_family", "Rex"))

        res = self.client.post(target_url, data=json.dumps(animal), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        return res.data

    def given_user_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="")

    def given_user_authenticated(self, username, password):
        auth_url = reverse("api-token-obtain-pair")
        res = self.client.post(auth_url, data=dict(username=username, password=password))
        access_token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def verify_expected_animal_count_and_get_results(self, expected_count: int):
        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), expected_count)
        return res.data["results"]

    def given_animal_exists(self, animal_params: Dict[str, str]) -> Animal:
        obj, created = Animal.objects.get_or_create(**animal_params)

        return obj

    def given_user_exists(self, username, email, password, is_staff=False, is_superuser=False) -> User:
        obj = User.objects.create_user(username=username, email=email, password=password, is_staff=is_staff,
                                       is_superuser=is_superuser)

        return obj