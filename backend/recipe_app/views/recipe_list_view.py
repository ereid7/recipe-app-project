from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from recipe_app.models import Recipe
from recipe_app.serializers import RecipeDetailSerializer, RecipeListSerializer

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
        serializer = RecipeListSerializer(recipes, many=True)  # Updated to use RecipeListSerializer
        return Response(serializer.data)

    def post(self, request) -> Response:
        """
        Create a new recipe.
    
        Args:
            request: The incoming HTTP request.
    
        Returns:
            A Response object containing the serialized data of the newly created recipe.
        """
        if 'url' in request.data and Recipe.objects.filter(Q(url=request.data['url'])).exists():
            return Response({'error': 'Recipe with this URL already exists.'}, status=status.HTTP_409_CONFLICT)
    
        serializer = RecipeDetailSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
