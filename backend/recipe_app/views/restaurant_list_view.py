from rest_framework.views import APIView
from rest_framework.response import Response
from recipe_app.models import Restaurant
from recipe_app.serializers import RestaurantSerializer

class RestaurantListView(APIView):
    """
    API view to fetch a list of restaurants.
    """

    def get(self, request):
        """
        Get a list of restaurants.

        Args:
            request: The HTTP request.

        Returns:
            Response: A JSON response containing the serialized restaurant data.
        """
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
