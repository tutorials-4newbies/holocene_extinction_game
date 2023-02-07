from django.urls import reverse
from rest_framework import status

from fauna.models import Animal
from fauna.tests.base import BaseTestCase


class AnimalDeactivatedViewTestCase(BaseTestCase):

    def test_animal_endpoint_doesnt_return_deactivated_animals(self):
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

        res = self.client.get(target_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)

        self.assertEqual(res.data["count"], 1)


