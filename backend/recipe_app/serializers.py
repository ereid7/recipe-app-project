from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient, Restaurant, RestaurantRecipe

class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for Ingredient model.
    """
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for RecipeIngredient model, including the related Ingredient.
    """
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient']

class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(child=serializers.CharField(), write_only=True)
    restaurants = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    ingredient_list = serializers.SerializerMethodField(read_only=True)
    restaurant_names = serializers.SerializerMethodField(read_only=True)  # Add this line

    class Meta:
        model = Recipe
        fields = ['id', 'url', 'title', 'description', 'instructions', 'ingredients', 'restaurants', 'ingredient_list', 'restaurant_names']  # Add 'restaurant_names' here

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        restaurant_ids = validated_data.pop('restaurants')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient_name in ingredients_data:
            ingredient_obj, created = Ingredient.objects.get_or_create(name=ingredient_name)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient_obj)

        for restaurant_id in restaurant_ids:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            RestaurantRecipe.objects.create(restaurant=restaurant, recipe=recipe)

        return recipe

    def get_ingredient_list(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return [ri.ingredient.name for ri in recipe_ingredients]

    def get_restaurant_names(self, obj):  # Add this method
        restaurant_recipes = RestaurantRecipe.objects.filter(recipe=obj)
        return [rr.restaurant.name for rr in restaurant_recipes]


class RecipeListSerializer(serializers.ModelSerializer):
    ingredients_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients_count']

    def get_ingredients_count(self, obj):
        return RecipeIngredient.objects.filter(recipe=obj).count()


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Restaurant model.
    """

    class Meta:
        model = Restaurant
        fields = '__all__'
