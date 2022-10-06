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

    def test_animal_endpoint_return_actual_animal(self):
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="",
                             taxonomy_order="",
                             taxonomy_family="",
                             )
        self.given_animal_exist(animal_params)
        target_url = reverse("animals-list")
        print(target_url)
        res = self.client.get(target_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]['name'], animal_params['name'])

    def test_animal_endpoint_returns_results_filter_by_periad(self):
        filter_period = Animal.PERIOD_CHOICES[0][0]
        first_animal_params = dict(
            period=Animal.PERIOD_CHOICES[6][0],
            extinction="Our very own",
            name="carrier pigeon",
            taxonomy_class="",
            taxonomy_order="",
            taxonomy_family="",
        )
        self.given_animal_exist(first_animal_params)

        secend_animal_params = dict(
            period=filter_period,
            extinction="mitior",
            name="dinosaur",
            taxonomy_class="",
            taxonomy_order="",
            taxonomy_family="",
        )
        self.given_animal_exist(secend_animal_params)

        target_url = reverse(f"animals-list")

        res = self.client.get(f"{target_url}?period={filter_period}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]['name'], secend_animal_params['name'])

    def test_authenticated_users_see_all_fields(self):
        self.given_user_exist(username="test_user", email="test@test.com", password="12345")
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="",
                             taxonomy_order="",
                             taxonomy_family="",
                             )
        self.given_animal_exist(animal_params)


        auth_url = reverse("api-token-obtain-pair")

        res = self.client.post(auth_url, data=dict(username="test_user", password="12345"))
        access_token = res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]['name'], animal_params['name'])
        self.assertIn("period", res.data["results"][0])
        self.assertIn("extinction", res.data["results"][0])
        self.assertIn("taxonomy_class", res.data["results"][0])
        self.assertIn("taxonomy_order", res.data["results"][0])
        self.assertIn("taxonomy_family", res.data["results"][0])

    def test_anonymous_users_see_only_name_and_period_fields(self):
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="",
                             taxonomy_order="",
                             taxonomy_family="",
                             )
        self.given_animal_exist(animal_params)

        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertIn("name", res.data["results"][0])
        self.assertEqual(res.data["results"][0]['name'], animal_params['name'])
        self.assertIn("period", res.data["results"][0])
        self.assertEqual(res.data["results"][0]['period'], animal_params['period'])
        self.assertNotIn("extinction", res.data["results"][0])
        self.assertNotIn("taxonomy_class", res.data["results"][0])
        self.assertNotIn("taxonomy_order", res.data["results"][0])
        self.assertNotIn("taxonomy_family", res.data["results"][0])

    def given_animal_exist(self, animal_params: Dict[str, str]) -> Animal:
        obj, created = Animal.objects.get_or_create(**animal_params)
        return obj

    def given_user_exist(self, username, email, password) -> User:
        obj = User.objects.create_user(username=username, email=email, password=password)
        return obj
