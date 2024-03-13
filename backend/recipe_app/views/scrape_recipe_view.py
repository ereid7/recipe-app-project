from bs4 import BeautifulSoup
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

class ScrapeRecipeView(APIView):
    """
    View for validating if a page contains a schema.org Recipe schema.
    """

    def get(self, request) -> Response:
        """
        Check if the provided URL contains a schema.org Recipe schema.
        https://schema.org/Recipe

        Args:
            request: The incoming HTTP request.

        Returns:
            A Response object indicating if the URL contains a valid recipe schema and returning recipe information if found.
        """
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, 'html.parser')

            script_tags = soup.find_all('script', type='application/ld+json')
            for script_tag in script_tags:
                try:
                    schema_data = json.loads(script_tag.string)
                    if isinstance(schema_data, list):
                        for item in schema_data:
                            if "@type" in item and "Recipe" in item["@type"]:
                                # Valid recipe schema found, return recipe information
                                recipe_info = {
                                    "title": item.get("name", ""),
                                    "description": item.get("description", ""),
                                    "ingredients": item.get("recipeIngredient", []),
                                }
                                return Response({'message': 'Valid recipe schema found', 'recipe': recipe_info}, status=status.HTTP_200_OK)
                    elif "@type" in schema_data and "Recipe" in schema_data["@type"]:
                        # Valid recipe schema found, return recipe information
                        recipe_info = {
                            "title": schema_data.get("name", ""),
                            "description": schema_data.get("description", ""),
                            "ingredients": schema_data.get("recipeIngredient", []),
                        }
                        return Response({'message': 'Valid recipe schema found', 'recipe': recipe_info}, status=status.HTTP_200_OK)
                except json.JSONDecodeError:
                    pass

            # No valid recipe schema found
            return Response({'error': 'Valid recipe schema not found'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
