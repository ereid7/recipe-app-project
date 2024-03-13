import json
import responses
from bs4 import BeautifulSoup
from rest_framework.test import APITestCase
from rest_framework import status

class ScrapeRecipeViewTestCase(APITestCase):
    @responses.activate
    def test_valid_recipe_url_format_1(self):
        mock_html = """
        <html>
            <head></head>
            <body>
                <script type="application/ld+json">
                    {
                        "@context": "https://schema.org/",
                        "@type": "Recipe",
                        "name": "Test Recipe",
                        "description": "Test Description",
                        "recipeIngredient": ["Ingredient 1", "Ingredient 2"],
                        "recipeInstructions": [
                            {"@type": "HowToStep", "text": "Step 1"},
                            {"@type": "HowToStep", "text": "Step 2"}
                        ]
                    }
                </script>
            </body>
        </html>
        """

        # Add the mocked response
        responses.add(responses.GET, "https://www.example.com/valid_recipe", body=mock_html, status=200)

        # Make a GET request to the ScrapeRecipeView with the mocked URL
        response = self.client.get("/api/scrape-recipe/", {"url": "https://www.example.com/valid_recipe"})

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected message
        self.assertEqual(response.data['message'], 'Valid recipe schema found')

        # Assert that the recipe information is present in the response
        self.assertIn('recipe', response.data)
        recipe_info = response.data['recipe']
        self.assertEqual(recipe_info['title'], 'Test Recipe')
        self.assertEqual(recipe_info['description'], 'Test Description')
        self.assertEqual(recipe_info['ingredients'], ['Ingredient 1', 'Ingredient 2'])
        self.assertEqual(recipe_info['instructions'], 'Step 1 Step 2')

    @responses.activate
    def test_valid_recipe_url_format_2(self):
        mock_html = """
        <html>
            <head></head>
            <body>
                <script type="application/ld+json">
                    {
                        "@context": "http://schema.org",
                        "@type": ["Recipe","NewsArticle"],
                        "name": "Easy Ground Beef Recipe",
                        "description": "Quick and simple ground beef recipe",
                        "recipeIngredient": ["Ground beef", "Onion", "Garlic"],
                        "recipeInstructions": [
                            {"@type": "HowToStep", "text": "Brown the beef, onion, and garlic."},
                            {"@type": "HowToStep", "text": "Add seasoning and cook until done."}
                        ]
                    }
                </script>
            </body>
        </html>
        """
    
        # Add the mocked response
        responses.add(responses.GET, "https://www.example.com/valid_recipe", body=mock_html, status=200)
    
        # Make a GET request to the ScrapeRecipeView with the mocked URL
        response = self.client.get("/api/scrape-recipe/", {"url": "https://www.example.com/valid_recipe"})
    
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        # Assert that the response contains the expected message
        self.assertEqual(response.data['message'], 'Valid recipe schema found')
    
        # Assert that the recipe information is present in the response
        self.assertIn('recipe', response.data)
        recipe_info = response.data['recipe']
        self.assertEqual(recipe_info['title'], 'Easy Ground Beef Recipe')
        self.assertEqual(recipe_info['description'], 'Quick and simple ground beef recipe')
        self.assertEqual(recipe_info['ingredients'], ['Ground beef', 'Onion', 'Garlic'])
        self.assertEqual(recipe_info['instructions'], 'Brown the beef, onion, and garlic. Add seasoning and cook until done.')


    def test_missing_url_parameter(self):
        # Make a GET request to the ScrapeRecipeView without providing the URL parameter
        response = self.client.get("/api/scrape-recipe/")

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the expected error message
        self.assertEqual(response.data['error'], 'URL is required')

    @responses.activate
    def test_invalid_recipe_url(self):
        # Mock the response with an empty script element (no recipe schema)
        mock_html = """
        <html>
            <head></head>
            <body>
                <script type="application/ld+json"></script>
            </body>
        </html>
        """
    
        # Add the mocked response
        responses.add(responses.GET, "https://www.example.com/invalid_recipe", body=mock_html, status=200)
    
        # Make a GET request to the ScrapeRecipeView with the mocked URL
        response = self.client.get("/api/scrape-recipe/", {"url": "https://www.example.com/invalid_recipe"})
    
        # Assert that the response status code is 422 UNPROCESSABLE ENTITY
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
    
        # Assert that the response contains the expected error message
        self.assertEqual(response.data['error'], 'Valid recipe schema not found')


    @responses.activate
    def test_exception_handling(self):
        # Mock an exception when making the request
        responses.add(responses.GET, "https://www.example.com/exception_recipe", body=Exception('Test exception'))

        # Make a GET request to the ScrapeRecipeView with the mocked URL
        response = self.client.get("/api/scrape-recipe/", {"url": "https://www.example.com/exception_recipe"})

        # Assert that the response status code is 500 INTERNAL SERVER ERROR
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Assert that the response contains the expected error message
        self.assertEqual(response.data['error'], 'Test exception')
