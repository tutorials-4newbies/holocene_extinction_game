import json
from typing import Dict

from django.contrib.auth.models import User
from configurations.management import call_command
from django.urls import reverse
from rest_framework import status

from fauna.models.animal import Animal
from fauna.tests.base import BaseTestCase


# Create your tests here.

class ResurrectionTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.admin_user = self.given_user_exists(username="admin_user",
                                                 email="admin@example.com",
                                                 password="12345",
                                                 is_staff=True,
                                                 is_superuser=True)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_resurrect_command(self):
        """
        create an animal
        call resurrect without god mode
        verify it's still dead
        call resurrect with god mode
        it's alive!
        """
        animal_params = dict(period=Animal.PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="Aves",
                             creator_id=self.admin_user.id,
                             taxonomy_order="Columbiformes",
                             taxonomy_family="Columbidae")
        # Arrange, Act, Assert == Given, When, Then
        self.given_animal_exists(animal_params)
        res = call_command("resurrect")
        animal = Animal.objects.get(name="carrier pigeon")
        self.assertFalse(animal.its_alive)

        res = call_command("resurrect", "--god_mode")
        animal = Animal.objects.get(name="carrier pigeon")
        self.assertTrue(animal.its_alive)