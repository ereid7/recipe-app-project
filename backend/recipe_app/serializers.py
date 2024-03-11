from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient

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

class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipe model, including related ingredients.
    """
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'ingredients']
