from typing import Dict

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
        animal_param = dict(period=Animal.PERIOD_CHOICES[6][0],
                            extinction="Our very own",
                            name="carrier pigeon",
                            taxonomy_class="Aves",
                            taxonomy_order="Columbiformes",
                            taxonomy_family="Columbidae"
                            )
        self.given_animal_exists(animal_param)
        target_url = reverse("animals-list")
        print(target_url)
        res = self.client.get(target_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)

    def given_animal_exists(self, animal_param: Dict[str, str]):
        obj, created = Animal.objects.get_or_create(**animal_param)
        return obj
