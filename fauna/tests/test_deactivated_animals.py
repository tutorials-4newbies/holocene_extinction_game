from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

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
        first_animal = res.data["results"][0]
        self.assertEqual(res.data["count"], 1)
        user = self.given_user_exists(username="test_user", email="test@example.com", password="12345")
        self.given_user_authenticated("test_user", "12345")
        res_data = self.when_animal_is_deactivated(first_animal["id"])

        res = self.client.get(target_url)
        self.assertEqual(res.data["count"], 0)
        
        self.act_as_admin_user()
        admin_target_url = reverse("admin:fauna_animal_changelist")
        admin_res = self.client.get(admin_target_url)
        self.assertOkResponse(res)
        self.assertEqual(len(admin_res.context_data["cl"].result_list), 0)

    def when_animal_is_deactivated(self, animal_id: int):
        target_url = reverse("animals-deactivate", args=[animal_id])
        res = self.client.post(target_url)
        self.assertOkResponse(res)
        return res.data

    def assertOkResponse(self, res: Response):
        self.assertIn(res.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def act_as_admin_user(self):
        self.given_user_authenticated(username=self.admin_user.username, password="12345")
        self.client.login(username=self.admin_user.username, password="12345")
