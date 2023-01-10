import json
from django.urls import reverse
from django.test.utils import override_settings
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

        # Get Animal dashboard data
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

    @override_settings(DEBUG=True)
    def test_optimized_likes_count(self):
        animals = []
        # Create 1000 animals
        names = list(range(1, 1000))
        for name in names:
            animals.append(Animal(
                name=name,
                period="PERMIAN",
                extinction="K/t",
                taxonomy_class="Dinsourses",
                taxonomy_order="Thripods",
                taxonomy_family="Rex",
                creator=self.admin_user,
            ))
        Animal.objects.bulk_create(animals)


        # Add users
        first_user = self.given_user_exists(username="first_user", email="first@example.com", password="12345")
        second_user = self.given_user_exists(username="second_user", email="second@example.com", password="12345")
        third_user = self.given_user_exists(username="third_user", email="third_user@example.com", password="12345")

        # Choose and use one of the animals
        first_animal_id = 1

        first_animal_like_url = reverse("animals-like", args=[first_animal_id])

        # Add a like with the first user
        self.given_user_authenticated(first_user.username, "12345")
        res = self.client.post(first_animal_like_url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        data_url = reverse("animals-users")
        res = self.client.get(data_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)



