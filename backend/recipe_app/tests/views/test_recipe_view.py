from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from recipe_app.models import Recipe
from recipe_app.serializers import RecipeDetailSerializer
from recipe_app.views import RecipeView


class TestRecipeViewGet(APITestCase):
    def setUp(self):
        self.url = '/api/recipes/'

    @patch('recipe_app.views.Recipe.objects.get')
    def test_get_existing_recipe(self, mock_get):
        mock_recipe = Recipe(id=1, title='Test Recipe', description='Test Description')
        mock_get.return_value = mock_recipe

        response = self.client.get('/api/recipes/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get.assert_called_once_with(pk=1)

    @patch('recipe_app.views.Recipe.objects.get')
    def test_get_nonexistent_recipe(self, mock_get):
        mock_get.side_effect = Recipe.DoesNotExist

        response = self.client.get('/api/recipes/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
