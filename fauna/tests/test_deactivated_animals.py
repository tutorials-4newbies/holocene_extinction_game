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

        self.assertEqual(res.data["count"], 1)
        existing_animal_id = res.data["results"][0]["id"]

        user = self.given_user_exists(username="test_user", email="test@example.com", password="12345")
        self.given_user_authenticated("test_user", "12345")

        self.when_animal_is_deactivated(existing_animal_id)

        res = self.client.get(target_url)
        self.assertIn("results", res.data)

        self.assertEqual(res.data["count"], 0)

        self.when_admin_user_logs_in()

        res_admin_data = self.get_animals_data_from_admin()
        self.assertEqual(res_admin_data.context_data["cl"].full_result_count, 0)

        deactivated_animal = Animal.unfiltered.get(name=animal_params["name"])
        deactivated_animal.its_alive = True
        deactivated_animal.save()

        res = self.client.get(target_url)
        self.assertEqual(res.data["count"], 1)

    def when_animal_is_deactivated(self, existing_animal_id: int):
        target_url = reverse("animals-deactivate", args=[existing_animal_id])
        res = self.client.post(target_url)
        self.assertResOk(res)
        return res

    def assertResOk(self, res: Response):
        self.assertIn(res.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def when_admin_user_logs_in(self):
        self.given_user_authenticated(self.admin_user.username, "12345")
        self.client.login(username=self.admin_user.username, password="12345")

    def get_animals_data_from_admin(self):
        target_url = reverse("admin:fauna_animal_changelist")
        res = self.client.get(target_url)
        self.assertResOk(res)
        return res
