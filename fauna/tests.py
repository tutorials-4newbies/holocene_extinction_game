from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class AnimalTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_empty_list_of_animals_on_endpoint(self):
        res = self.client.get(reverse("animals-list"))
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(len(res.data), 0)