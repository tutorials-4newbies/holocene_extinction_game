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
        animals = []
        # Create 1000 animals as a list
        required_animals_length = 1000
        names = list(range(0, required_animals_length))
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
        # Bulk insert bypassing our API
        Animal.objects.bulk_create(animals)

        data_url = reverse("animals-creators")
        res = self.client.get(data_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEqual(len(data), required_animals_length)

        # Test the first result to see the structure of the returned data
        animal = data[0]
        self.assertEqual(animal.get("name"), "0")
        self.assertEqual(animal.get('extinction'), "K/t")
        creator = animal.get("creator")
        self.assertEqual(creator.get("id"), self.admin_user.id)
        self.assertEqual(creator.get("username"), self.admin_user.username)
        self.assertEqual(creator.get("email"), self.admin_user.email)
