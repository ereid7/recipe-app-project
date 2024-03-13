from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recipe_app.models import Recipe
from recipe_app.serializers import RecipeSerializer

class RecipeListView(APIView):
    """
    View for retrieving a list of recipes.
    """
    def get(self, request) -> Response:
        """
        Retrieve a list of all recipes.

        Args:
            request: The incoming HTTP request.

        Returns:
            A Response object containing the serialized list of recipes.
        """
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
