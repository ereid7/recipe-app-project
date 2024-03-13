from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from recipe_app.models import Recipe
from recipe_app.serializers import RecipeListSerializer, RecipeDetailSerializer
from django.urls import reverse

class TestRecipeListViewGet(APITestCase):
    def setUp(self):
        self.url = reverse('recipe_list')

    @patch('recipe_app.views.Recipe.objects.all')
    def test_get_all_recipes(self, mock_recipe_all):
        mock_recipes = [
            Recipe(id=1, title='Recipe 1', description='Description 1'),
            Recipe(id=2, title='Recipe 2', description='Description 2')
        ]
        mock_recipe_all.return_value = mock_recipes

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, RecipeListSerializer(mock_recipes, many=True).data)

class TestRecipeListViewPost(APITestCase):
    def setUp(self):
        self.url = reverse('recipe_list')

    @patch('recipe_app.views.Recipe.objects.filter')
    @patch('recipe_app.views.RecipeDetailSerializer')
    def test_create_new_recipe_success(self, mock_serializer, mock_recipe_filter):
        mock_recipe_filter.return_value.exists.return_value = False
        mock_serializer.return_value.is_valid.return_value = True
    
        data = {
            'title': 'New Recipe',
            'description': 'Description of new recipe',
            'url': 'https://www.mockurl.com',
            'ingredients': [
                'ingredient1',
                'ingredient2'
            ],
            'instructions': 'mock instructions',
            'restaurants': []
        }
        response = self.client.post(self.url, data, format='json')
    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        expected_data = {
            'title': 'New Recipe',
            'url': 'https://www.mockurl.com',
            'description': 'Description of new recipe',
            'instructions': 'mock instructions',
            'ingredient_list': ['ingredient1', 'ingredient2'],
            'restaurant_names': []
        }

        for key, value in expected_data.items():
            if key != 'id':
                self.assertEqual(response.data[key], value)

    @patch('recipe_app.views.Recipe.objects.filter')
    def test_create_new_recipe_failure_url_exists(self, mock_recipe_filter):
        # Mock that a recipe with the same URL exists
        mock_recipe_filter.return_value.exists.return_value = True
    
        # Data with an existing URL
        data = {'title': 'New Recipe', 'description': 'Description of new recipe', 'url': 'existing_url'}
    
        # Make a POST request
        response = self.client.post(self.url, data, format='json')
    
        # Assert that the response status code is 409 CONFLICT
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
        # Assert that the response contains the expected error message
        self.assertEqual(response.data, {'error': 'Recipe with this URL already exists.'})

    def test_create_new_recipe_failure_invalid_data(self):
        request_data = {
            'description': 'Test Description',
        }
    
        # Make a POST request to create a new recipe with invalid data
        response = self.client.post("/api/recipes/", request_data)
    
        # Assert that the response status code is 422 UNPROCESSABLE ENTITY
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
    
        # Assert that the response contains the expected error message for the 'url' field
        self.assertEqual(response.data['url'], ['This field is required.'])
