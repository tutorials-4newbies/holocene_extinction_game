import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fauna.models import Animal
from fauna.tests.base import given_user_exists, given_user_authenticated, given_user_unauthenticated


class DashBoardTestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = given_user_exists(username="admin_user",
                                            email="admin@example.com",
                                            password="12345",
                                            is_staff=True,
                                            is_superuser=True)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_get_animals_with_most_likes(self):
        first_user = given_user_exists(username="test_user", email="test@example.com", password="12345")
        second_user = given_user_exists(username="second_user", email="second@example.com", password="12345")

        # Now authenticate and create animal as first user
        given_user_authenticated(self.client, "admin_user", "12345")
        animal_data = self.when_authenticated_user_creates_animal_via_api()
        given_user_unauthenticated(self.client)
        animal_id = animal_data["id"]
        animal_url = reverse("animals-detail", args=[animal_id])

        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 0)
        self.assertEqual(res.data["is_liked"], False)
        like_target_url = reverse("animals-like", args=[animal_id])

        res = self.client.post(like_target_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        given_user_authenticated(self.client, "test_user", "12345")
        res = self.client.post(like_target_url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the animal
        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 1)
        self.assertEqual(res.data["is_liked"], True)  # As I haved LIKED the animal

        # Now switch users
        given_user_authenticated(self.client, "second_user", "12345")

        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 1)
        self.assertEqual(res.data["is_liked"], False)  # I'm not the creating user, so shoul;dn't show that I have liked

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