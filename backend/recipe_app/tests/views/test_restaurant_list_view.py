from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from recipe_app.models import Restaurant
from recipe_app.serializers import RestaurantSerializer
from recipe_app.views import RestaurantListView


class TestRestaurantListViewGet(APITestCase):
    def setUp(self):
        self.url = reverse('restaurant_list')

    @patch('recipe_app.views.Restaurant.objects.all')
    def test_get_all_restaurants(self, mock_all):
        mock_restaurants = [
            Restaurant(id=1, name='Restaurant 1', location='Location 1'),
            Restaurant(id=2, name='Restaurant 2', location='Location 2')
        ]
        mock_all.return_value = mock_restaurants

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_all.assert_called_once()

        expected_data = RestaurantSerializer(mock_restaurants, many=True).data
        self.assertEqual(response.data, expected_data)

    @patch('recipe_app.views.Restaurant.objects.all')
    def test_get_empty_restaurant_list(self, mock_all):
        mock_all.return_value = []

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_all.assert_called_once()
        self.assertEqual(response.data, [])
