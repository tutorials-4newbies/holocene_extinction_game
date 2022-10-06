from typing import Dict

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
from fauna.models import Animal


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

    def test_animal_endpoint(self):
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Oh no",
                             name="carrier pigeon",
                             taxonomy_class="Aves",
                             taxonomy_order="Columbiformes",
                             taxonomy_family="Columbidae")
        self.given_animal_exists(animal_params)
        target_url = reverse("animals-list")
        print(target_url)
        res = self.client.get(target_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        first_animal = res.data["results"][0]
        self.assertIn('period', first_animal)

        self.assertEqual(first_animal["name"], animal_params["name"])

    def test_animal_endpoints_returns_results_filtered_by_period(self):
        animal1_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                              extinction="Oh no",
                              name="carrier pigeon",
                              taxonomy_class="Aves",
                              taxonomy_order="Columbiformes",
                              taxonomy_family="Columbidae")
        animal2_params = dict(period=Animal.PERIOD_CHOICES[5][0],
                              extinction="Oh no",
                              name="carrier pigeon",
                              taxonomy_class="Aves",
                              taxonomy_order="Columbiformes",
                              taxonomy_family="Columbidae")

        self.given_animal_exists(animal1_params)
        self.given_animal_exists(animal2_params)

        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}?period={Animal.PERIOD_CHOICES[5][0]}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)

    def test_authenticated_users_see_all_fields(self):
        self.given_user_exists(username="test_user", email="test@test.com", password="test_password")
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Oh no",
                             name="carrier pigeon",
                             taxonomy_class="Aves",
                             taxonomy_order="Columbiformes",
                             taxonomy_family="Columbidae")
        self.given_animal_exists(animal_params)
        auth_url = reverse('api-token-obtain-pair')
        res = self.client.post(auth_url, data=dict(username="test_user", password="test_password"))
        access_token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        target_url = reverse("animals-list")

        res = self.client.get(target_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        self.assertIn('period', res.data["results"][0])
        self.assertIn('taxonomy_family', res.data["results"][0])

    def given_animal_exists(self, animal_params: Dict[str, str]):
        new_animal, created = Animal.objects.get_or_create(**animal_params)
        return new_animal

    def given_user_exists(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return user
