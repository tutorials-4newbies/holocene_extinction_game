from django.urls import reverse
from rest_framework import status
from fauna.models import Animal
from fauna.tests.base import BaseAPITestCase


class DashBoardTestCase(BaseAPITestCase):
    def test_get_animals_with_most_likes(self):
        # Admin login
        self.given_user_authenticated("admin_user", "12345")
        # Create 6 animals
        triceratops = self.when_authenticated_user_creates_animal_via_api(name="Triceratops_123454251")
        archaeopteryx = self.when_authenticated_user_creates_animal_via_api(name="Archaeopteryx")
        brachiosaurus = self.when_authenticated_user_creates_animal_via_api(name="Brachiosaurus")
        velociraptor = self.when_authenticated_user_creates_animal_via_api(name="Velociraptor")
        spinosaurus = self.when_authenticated_user_creates_animal_via_api(name="Spinosaurus")
        stegosaurus = self.when_authenticated_user_creates_animal_via_api(name="Stegosaurus")
        bee = self.when_authenticated_user_creates_animal_via_api(name="bee")

        # Admin logout
        self.given_user_unauthenticated()

        # Add users
        first_user = self.given_user_exists(username="first_user", email="first@example.com", password="12345")
        second_user = self.given_user_exists(username="second_user", email="second@example.com", password="12345")
        third_user = self.given_user_exists(username="third_user", email="third_user@example.com", password="12345")

        # Choose and use one of the animals
        stegosaurus_id = stegosaurus["id"]
        stegosaurus_url = reverse("animals-detail", args=[stegosaurus_id])
        like_target_url = reverse("animals-like", args=[stegosaurus_id])

        # Add a like with the first user
        self.given_user_authenticated(first_user.username, "12345")
        res = self.client.post(like_target_url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Add a like with the second_user
        self.given_user_authenticated(second_user.username, "12345")
        res = self.client.post(like_target_url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Add a like with the third_user
        self.given_user_authenticated(third_user.username, "12345")
        res = self.client.post(like_target_url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Check that the chosen animal has 3 likes
        res = self.client.get(stegosaurus_url)
        self.assertEqual(res.data["likes_count"], 3)

        # # Get Animal dashboard data
        dashboard_url = reverse("animals-dashboard")
        res = self.client.get(dashboard_url)
        dashboard_data = res.data
        self.assertEqual(dashboard_data['animals_count'], 7)
        self.assertEqual(dashboard_data['avg_name_length'], 12)
        self.assertEqual(dashboard_data['longest_name'], triceratops['name'])
        self.assertEqual(dashboard_data['shortest_name'], bee['name'])
        self.assertEqual(dashboard_data['most_liked_animal_name'], stegosaurus["name"])
        self.assertEqual(len(dashboard_data['top_3_liked_animals']), 3)
        top_animal = dashboard_data['top_3_liked_animals'][0]
        self.assertEqual(top_animal["id"], stegosaurus["id"])

    def test_get_animals_with_creator_endpoint(self):
        # TODO: Create lots of animals
        required_animals_length = 5

        # get the data
        data_url = reverse("animals-creators")
        res = self.client.get(data_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), required_animals_length)

        # TODO: Test the result to see the structure of the returned data
        # should be
        # [
        #     {
        #         "id": "animal id",
        #         "name": "some name",
        #         "extinction": "ext",
        #         "creator": {
        #             "id": "creator id",
        #             "username": "creator username",
        #             "email": "creator email",
        #         }
        #     }
        # ]

