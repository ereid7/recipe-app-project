from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from recipe_app.models import Recipe
from recipe_app.serializers import RecipeSerializer

class RecipeView(APIView):
    """
    View for retrieving a single recipe and creating a new recipe.
    """

    def get_permissions(self):
        """
        Set permissions based on the request method.
        """
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

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
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request) -> Response:
        """
        Create a new recipe.

        Args:
            request: The incoming HTTP request.

        Returns:
            A Response object containing the serialized data of the newly created recipe.
        """
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
