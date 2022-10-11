import http
from typing import Dict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fauna.models import Animal


# Create your tests here.

class AnimalViewTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                                  extinction="Our very own",
                                  name="carrier pigeon",
                                  taxonomy_class="Aves",
                                  taxonomy_order="Columbiformes",
                                  taxonomy_family="Columbidae")

    def tearDown(self) -> None:
        super().tearDown()

    def test_animal_endpoint_returns_empty_list(self):
        res = self.when_requesting_animal_list()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 0)

    def test_animal_endpoint_returns_actual_animals(self):
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(self.animal_params)
        res = self.when_requesting_animal_list()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        first_animal = res.data["results"][0]

        self.assertEqual(first_animal["name"], "carrier pigeon")

    def test_authenticated_user_gets_full_animal_list(self):
        self.given_user_exists()
        self.given_user_logged_in()
        self.given_animal_exists(self.animal_params)
        res = self.when_requesting_animal_list()
        self.verify_animal_has_properties(res, ("name", "extinction", "period", "taxonomy_class",
                                                "taxonomy_order", "taxonomy_family"))

    def test_anonymous_user_gets_partial_data_on_animals(self):
        self.given_animal_exists(self.animal_params)
        res = self.when_requesting_animal_list()
        self.verify_animal_has_properties(res, ("name", "extinction", "period"))

    def given_animal_exists(self, animal_params: Dict[str, str]) -> Animal:
        obj, created = Animal.objects.get_or_create(**animal_params)
        return obj

    def given_user_exists(self, username: str = "user", password: str = "1234") -> User:
        user = User.objects.create_user(username=username, password=password)
        return user

    def given_user_logged_in(self, username: str = "user", password: str = "1234") -> None:
        res = self.when_requesting_auth_token(username, password)
        if res.status_code != http.HTTPStatus.OK:
            raise ValueError(f'Login failed, response status code is {res.status_code}\nContent reads: {res.content}')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])
        self.client.extra = {'refresh': res.data['refresh']}

    def verify_animal_has_properties(self, res, expected_keys: tuple[str, ...]):
        res_animal = res.data["results"][0]
        self.assertTrue(all(key in res_animal.keys() for key in expected_keys))

    def when_requesting_auth_token(self, username: str = "user", password: str = "1234"):
        return self.client.post(reverse('api-token-obtain-pair'), data={"username": username, "password": password})

    def when_requesting_animal_list(self):
        return self.client.get(reverse("animals-list"))
