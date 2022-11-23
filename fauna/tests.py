import json
from typing import Dict

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fauna.models import Animal


# Create your tests here.

class AnimalViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = self.given_user_exists(username="admin_user",
                                                 email="admin@example.com",
                                                 password="12345",
                                                 is_staff=True,
                                                 is_superuser=True)
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
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="Aves",
                             creator_id=self.admin_user.id,
                             taxonomy_order="Columbiformes",
                             taxonomy_family="Columbidae")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)
        target_url = reverse("animals-list")
        print(target_url)
        res = self.client.get(target_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        first_animal = res.data["results"][0]

        self.assertEqual(first_animal["name"], "carrier pigeon")

    def test_animal_endpoints_returns_results_filtered_by_period(self):
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="Aves",
                             creator=self.admin_user,
                             taxonomy_order="Columbiformes",
                             taxonomy_family="Columbidae")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)

        animal_params = dict(period=Animal.PERIOD_CHOICES[5][0],
                             extinction="K/t",
                             name="T-rex",
                             creator_id=self.admin_user.id,
                             taxonomy_class="Dinsourses",
                             taxonomy_order="Thripods",
                             taxonomy_family="Rex")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)

        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}?period={Animal.PERIOD_CHOICES[5][0]}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        first_animal = res.data["results"][0]
        self.assertEqual(first_animal["name"], "T-rex")
        self.assertNotIn("taxonomy_family", first_animal)

    def test_authenticated_users_see_all_fields(self):
        # Create user
        # create animal
        # Login
        # get with authenticated user animal and verify it has period, and has taxonomy_family
        self.given_user_exists(username="test_user", email="test@example.com", password="12345")
        animal_params = dict(period=Animal.PERIOD_CHOICES[5][0],
                             extinction="K/t",
                             name="T-rex",
                             creator=self.admin_user,
                             taxonomy_class="Dinsourses",
                             taxonomy_order="Thripods",
                             taxonomy_family="Rex")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)
        auth_url = reverse("api-token-obtain-pair")
        res = self.client.post(auth_url, data=dict(username="test_user", password="12345"))
        access_token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["count"], 1)
        first_animal = res.data["results"][0]
        self.assertIn("taxonomy_family", first_animal)

    def test_authenticated_user_can_create(self):
        self.verify_expected_animal_count_and_get_results(0)
        target_url = reverse("animals-list")
        animal = dict(period=Animal.PERIOD_CHOICES[5][0],
                      extinction="K/t",
                      name="T-rex",
                      taxonomy_class="Dinsourses",
                      taxonomy_order="Thripods",
                      taxonomy_family="Rex")
        res = self.client.post(target_url, data=json.dumps(animal), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        user = self.given_user_exists(username="test_user", email="test@example.com", password="12345")
        self.given_user_authenticated("test_user", "12345")

        res = self.client.post(target_url, data=json.dumps(animal), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        results = self.verify_expected_animal_count_and_get_results(1)

        first_animal = results[0]
        self.assertEqual(first_animal["creator"], user.id)

    def test_delete_only_possible_for_creator_or_admin(self):
        target_url = reverse("animals-list")
        animal = dict(period=Animal.PERIOD_CHOICES[5][0],
                      extinction="K/t",
                      name="T-rex",
                      taxonomy_class="Dinsourses",
                      taxonomy_order="Thripods",
                      taxonomy_family="Rex")
        first_user = self.given_user_exists(username="test_user", email="test@example.com", password="12345")
        second_user = self.given_user_exists(username="second_user", email="second@example.com", password="12345")

        # Now authenticate and create animal as first user
        self.given_user_authenticated("test_user", "12345")

        res = self.client.post(target_url, data=json.dumps(animal), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.verify_expected_animal_count_and_get_results(1)

        # switch users
        self.given_user_authenticated("second_user", "12345")

        # Verify animal deletion failed for second user
        delete_target_url = reverse("animals-detail", args=[res.data["id"]])
        # /api/fauna/animals/1/
        res = self.client.delete(delete_target_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.verify_expected_animal_count_and_get_results(1)
        # Now for the prestige part, we'll switch users
        self.given_user_authenticated("test_user", "12345")
        res = self.client.delete(delete_target_url)

        # And see the animal deleted
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.verify_expected_animal_count_and_get_results(0)

        res = self.client.post(target_url, data=json.dumps(animal), content_type="application/json")

        delete_target_url = reverse("animals-detail", args=[res.data["id"]])

        self.verify_expected_animal_count_and_get_results(1)

        self.given_user_authenticated(self.admin_user.username, "12345")

        res = self.client.delete(delete_target_url)

        # And see the animal deleted
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.verify_expected_animal_count_and_get_results(0)

    def test_animal_like_behavior(self):
        # create animal
        # create user
        # should try to like and fail
        # the user should be authenticated
        # get the animal verify like count == 0 , is_liked = False
        # should try to like
        # get the animal - verify like count == 1, is_liked = True
        # different user login
        # get the animal - verify like count == 1, is_liked = False
        first_user = self.given_user_exists(username="test_user", email="test@example.com", password="12345")
        second_user = self.given_user_exists(username="second_user", email="second@example.com", password="12345")

        # Now authenticate and create animal as first user
        self.given_user_authenticated("admin_user", "12345")
        animal_data = self.when_authenticated_user_creates_animal_via_api()
        self.given_user_unauthenticated()
        animal_id = animal_data["id"]
        animal_url = reverse("animals-detail", args=[animal_id])

        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 0)
        self.assertEqual(res.data["is_liked"], False)
        like_target_url = reverse("animals-like", args=[animal_id])

        res = self.client.post(like_target_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.given_user_authenticated("test_user", "12345")
        res = self.client.post(like_target_url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        #get the animal
        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 1)
        self.assertEqual(res.data["is_liked"], True) #As I haved LIKED the animal

        # Now switch users
        self.given_user_authenticated("second_user", "12345")


        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 1)
        self.assertEqual(res.data["is_liked"], False) #I'm not the creating user, so shoul;dn't show that I have liked

    def test_animal_unlike_behavior(self):
        # create animal
        # create user
        # the user should be authenticated
        # should try to like
        # get the animal - verify like count == 1, is_liked = True
        # should unlike
        # get the animal verify like count == 0 , is_liked = False
        # try to unlike AGAIN the animal and get a success
        # get the animal verify like count == 0 , is_liked = False
        first_user = self.given_user_exists(username="test_user", email="test@example.com", password="12345")

        # Now authenticate and create animal as admin user
        self.given_user_authenticated("admin_user", "12345")
        animal_data = self.when_authenticated_user_creates_animal_via_api()
        self.given_user_unauthenticated()


        animal_id = animal_data["id"]
        animal_url = reverse("animals-detail", args=[animal_id])

        like_target_url = reverse("animals-like", args=[animal_id])
        unlike_target_url = reverse("animals-unlike", args=[animal_id])

        self.given_user_authenticated("test_user", "12345")
        res = self.client.post(like_target_url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 1)
        self.assertEqual(res.data["is_liked"], True)  # As I haved LIKED the animal

        res = self.client.post(unlike_target_url)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 0)
        self.assertEqual(res.data["is_liked"], False)  # As I haved UNLIKED the animal

        # Now verify unliking without a current like doesn't break the system
        res = self.client.post(unlike_target_url)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(animal_url)
        self.assertEqual(res.data["likes_count"], 0)
        self.assertEqual(res.data["is_liked"], False)  # As I haved UNLIKED the animal





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

    def given_user_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
    def given_user_authenticated(self, username, password):
        auth_url = reverse("api-token-obtain-pair")
        res = self.client.post(auth_url, data=dict(username=username, password=password))
        access_token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def verify_expected_animal_count_and_get_results(self, expected_count: int):
        target_url = reverse("animals-list")

        res = self.client.get(f"{target_url}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(len(res.data["results"]), expected_count)
        return res.data["results"]

    def given_animal_exists(self, animal_params: Dict[str, str]) -> Animal:
        obj, created = Animal.objects.get_or_create(**animal_params)

        return obj

    def given_user_exists(self, username, email, password, is_staff=False, is_superuser=False) -> User:
        obj = User.objects.create_user(username=username, email=email, password=password, is_staff=is_staff,
                                       is_superuser=is_superuser)

        return obj
