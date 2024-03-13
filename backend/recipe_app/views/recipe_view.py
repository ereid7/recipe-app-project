from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db import IntegrityError
from recipe_app.models import Recipe
from recipe_app.serializers import RecipeDetailSerializer

class RecipeView(APIView):
    """
    View for retrieving a single recipe and creating a new recipe.
    """

    def get(self, request, pk: int) -> Response:
        """
        Retrieve a single recipe by its primary key.

        Args:
            request: The incoming HTTP request.
            pk: The primary key of the recipe to retrieve.

        Returns:
            A Response object containing the serialized recipe data.
        """
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeDetailSerializer(recipe)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

