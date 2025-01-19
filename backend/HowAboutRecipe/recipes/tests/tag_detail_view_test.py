from rest_framework import status
from rest_framework.test import APITestCase
from recipes.models import Tag


class TagDetailViewTest(APITestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.base_link = "/api/recipes/tag/"
        self.link_tag1 = self.base_link + f"{self.tag1.id}/"
        self.link_tag2 = self.base_link + "12/"
        self.link_tag3 = self.link_tag1 + "blah/"

    def test_found_tag(self):
        response = self.client.get(self.link_tag1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], str(self.tag1.name))
        self.assertEqual(response.data['link'], str(self.link_tag1))

    def test_not_found_tag(self):
        response = self.client.get(self.link_tag2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_request(self):
        response = self.client.get(self.link_tag3)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
