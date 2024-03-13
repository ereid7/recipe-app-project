from recipe_app.models import Ingredient, Recipe, RecipeIngredient, Restaurant
from recipe_app.serializers import IngredientSerializer, RecipeDetailSerializer, RecipeListSerializer, RestaurantSerializer
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase

class IngredientSerializerTest(APITestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Flour", quantity="2 cups")

    def test_ingredient_serializer(self):
        # Test serialization of a single ingredient
        serializer = IngredientSerializer(self.ingredient)
        expected_data = {'name': 'Flour', 'quantity': '2 cups'}
        self.assertEqual(serializer.data, expected_data)

class RestaurantSerializerTest(APITestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", location="Test Location")

    def test_restaurant_serializer(self):
        # Test serialization of a single restaurant
        serializer = RestaurantSerializer(self.restaurant)
        expected_data = {
            'id': self.restaurant.id,
            'name': 'Test Restaurant',
            'location': 'Test Location'
        }
        self.assertEqual(serializer.data, expected_data)

class RecipeDetailSerializerTest(APITestCase):
    def setUp(self):
        self.ingredient1 = Ingredient.objects.create(name="Flour", quantity="2 cups")
        self.ingredient2 = Ingredient.objects.create(name="Sugar", quantity="1 cup")
        self.restaurant1 = Restaurant.objects.create(name="Test Restaurant 1", location="Test Location 1")
        self.restaurant2 = Restaurant.objects.create(name="Test Restaurant 2", location="Test Location 2")

        self.recipe_data = {
            "title": "Test Recipe",
            "description": "Test Description",
            "instructions": "Test Instructions",
            "url": "http://testrecipe.com",
            "ingredients": ["Flour", "Sugar"],
            "restaurants": [self.restaurant1.id, self.restaurant2.id]
        }

    def test_recipe_detail_serializer_create(self):
        # Test creation of a recipe through the serializer
        serializer = RecipeDetailSerializer(data=self.recipe_data)
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()

        self.assertEqual(recipe.title, "Test Recipe")
        self.assertEqual(recipe.description, "Test Description")
        self.assertEqual(recipe.instructions, "Test Instructions")
        self.assertEqual(recipe.url, "http://testrecipe.com")

        # Verify ingredients and restaurants were associated correctly
        self.assertEqual(recipe.recipeingredient_set.count(), 2)
        self.assertEqual(recipe.restaurantrecipe_set.count(), 2)
        ingredient_names = [ri.ingredient.name for ri in recipe.recipeingredient_set.all()]
        self.assertIn("Flour", ingredient_names)
        self.assertIn("Sugar", ingredient_names)
        restaurant_names = [rr.restaurant.name for rr in recipe.restaurantrecipe_set.all()]
        self.assertIn("Test Restaurant 1", restaurant_names)
        self.assertIn("Test Restaurant 2", restaurant_names)

class RecipeListSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.ingredient1 = Ingredient.objects.create(name="Flour", quantity="2 cups")
        cls.ingredient2 = Ingredient.objects.create(name="Sugar", quantity="1 cup")
        cls.recipe = Recipe.objects.create(title="Test Cake", description="A delicious cake")
        RecipeIngredient.objects.create(recipe=cls.recipe, ingredient=cls.ingredient1)
        RecipeIngredient.objects.create(recipe=cls.recipe, ingredient=cls.ingredient2)

    def test_recipe_list_serializer(self):
        """
        Test that the RecipeListSerializer correctly serializes recipe data, including the count of ingredients.
        """
        # Prepare data
        recipes = Recipe.objects.all()
        serializer = RecipeListSerializer(recipes, many=True)
        
        # Expected data format
        expected_data = [{
            'id': self.recipe.id,
            'title': 'Test Cake',
            'description': 'A delicious cake',
            'ingredients_count': 2
        }]
        
        # Test
        self.assertEqual(serializer.data, expected_data)

