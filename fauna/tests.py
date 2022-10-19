import json
from typing import Dict

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fauna.models import Animal


# Create your tests here.

class AnimalViewTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_animal_endpoint_returns_empty_list(self):
        target_url = reverse("animals-list")
        print(target_url)
        res = self.client.get(target_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 0)

    def test_animal_endpoint_returns_actual_animals(self):
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="Aves",
                             taxonomy_order="Columbiformes",
                             taxonomy_family="Columbidae")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)
        target_url = reverse("animals-list")
        print(target_url)
        res = self.client.get(target_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        first_animal = res.data["results"][0]

        self.assertEqual(first_animal["name"], "carrier pigeon")

    def test_animal_endpoints_returns_results_filtered_by_period(self):
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="Aves",
                             taxonomy_order="Columbiformes",
                             taxonomy_family="Columbidae")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)

        animal_params = dict(period=Animal.PERIOD_CHOICES[5][0],
                             extinction="K/t",
                             name="T-rex",
                             taxonomy_class="Dinsourses",
                             taxonomy_order="Thripods",
                             taxonomy_family="Rex")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)

        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}?period={Animal.PERIOD_CHOICES[5][0]}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        first_animal = res.data["results"][0]
        self.assertEqual(first_animal["name"], "T-rex")
        self.assertNotIn("taxonomy_family", first_animal)

    def test_authenticated_users_see_all_fields(self):
        # Create user
        # create animal
        # Login
        # get with authenticated user animal and verify it has period, and has taxonomy_family
        self.given_user_exists(username="test_user", email="test@example.com", password="12345")
        animal_params = dict(period=Animal.PERIOD_CHOICES[5][0],
                             extinction="K/t",
                             name="T-rex",
                             taxonomy_class="Dinsourses",
                             taxonomy_order="Thripods",
                             taxonomy_family="Rex")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)
        auth_url = reverse("api-token-obtain-pair")
        res = self.client.post(auth_url, data=dict(username="test_user", password="12345"))
        access_token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        first_animal = res.data["results"][0]
        self.assertIn("taxonomy_family", first_animal)

    def test_authenticated_user_can_create(self):
        # check animal not exists
        # try to create
        # check not exists
        # create user and authenticate
        # try to create
        # check animal exists
        self.verify_expected_animal_count(0)
        target_url = reverse("animals-list")
        animal = dict(period=Animal.PERIOD_CHOICES[5][0],
                      extinction="K/t",
                      name="T-rex",
                      taxonomy_class="Dinsourses",
                      taxonomy_order="Thripods",
                      taxonomy_family="Rex")
        res = self.client.post(target_url, data=json.dumps(animal), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.given_user_exists(username="test_user", email="test@example.com", password="12345")
        self.given_user_authenticated("test_user", "12345")

        res = self.client.post(target_url, data=json.dumps(animal), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.verify_expected_animal_count(1)
    def given_user_authenticated(self, username, password):
        auth_url = reverse("api-token-obtain-pair")
        res = self.client.post(auth_url, data=dict(username=username, password=password))
        access_token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def verify_expected_animal_count(self, expected_count: int):
        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), expected_count)

    def given_animal_exists(self, animal_params: Dict[str, str]) -> Animal:
        obj, created = Animal.objects.get_or_create(**animal_params)

        return obj

    def given_user_exists(self, username, email, password) -> User:
        obj = User.objects.create_user(username=username, email=email, password=password)

        return obj
