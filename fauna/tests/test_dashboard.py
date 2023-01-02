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
        # Admin login
        given_user_authenticated(self.client, "admin_user", "12345")

        # Create 6 animals
        #...
        stegosaurus = self.when_authenticated_user_creates_animal_via_api(name="Stegosaurus")

        # Admin logout
        given_user_unauthenticated(self.client)

        # Add users
        first_user = given_user_exists(username="first_user", email="first@example.com", password="12345")
        # ...

        # Choose and use one of the animals - the stegosaurus
        stegosaurus_id = stegosaurus["id"]
        like_target_url = reverse("animals-like", args=[stegosaurus_id])

        # Add a like with the first user


        # Add a like with the second_user


        # Add a like with the third_user

        # Check that the chosen animal has 3 likes
        stegosaurus_url = reverse("animals-detail", args=[stegosaurus_id])


        # Get Animal list which should be ordered by likes count
        # assert the order


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
