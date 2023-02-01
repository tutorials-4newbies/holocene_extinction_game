from django.contrib.auth import get_user_model

from fauna.models import Animal
from rest_framework.test import APITestCase


class ResurrectViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = self.given_user_exists(username="admin_user",
                                                 email="admin@example.com",
                                                 password="12345",
                                                 is_staff=True,
                                                 is_superuser=True)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def given_animal_exists(self, animal_params: Dict[str, str]) -> Animal:
        obj, created = Animal.objects.get_or_create(**animal_params)

        return obj

    def given_user_exists(self, username, email, password, is_staff=False, is_superuser=False) -> User:
        obj = get_user_model().objects.create_user(username=username, email=email, password=password, is_staff=is_staff,
                                                   is_superuser=is_superuser)

        return obj

    def test_resurrection_works(self):
        # create a dead animal
        # run the command
        # see it's resurrected
        # check the stdout
        pass