from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class AnimalViewsetTestCase(APITestCase):
    
    def setUp(self) -> None:
        super(AnimalViewsetTestCase, self).setUp()
    
    def tearDown(self) -> None:
        super(AnimalViewsetTestCase, self).tearDown()

    def test_animal_viewset_api_endpoint(self):
        res = self.client.get(reverse('animals-list'))
        self.assertEqual(res.status_code, 200)
        self.assertIn('results', res.json())
