from django.core.management.base import BaseCommand
from recipe_app.models import Restaurant, Recipe, RestaurantRecipe, Ingredient, RecipeIngredient

class Command(BaseCommand):
    help = 'Seeds the database with mock data'

    def handle(self, *args, **kwargs):
        # Create mock restaurants
        restaurant1 = Restaurant.objects.create(name='Restaurant 1', location='Location 1')
        restaurant2 = Restaurant.objects.create(name='Restaurant 2', location='Location 2')

        # Create mock recipes
        recipe1 = Recipe.objects.create(title='Recipe 1', description='Description 1', instructions='Instructions 1')
        recipe2 = Recipe.objects.create(title='Recipe 2', description='Description 2', instructions='Instructions 2')
        recipe3 = Recipe.objects.create(title='Recipe 3', description='Description 3', instructions='Instructions 3')

        # Create mock ingredients
        ingredient1 = Ingredient.objects.create(name='Ingredient 1', quantity='1 cup')
        ingredient2 = Ingredient.objects.create(name='Ingredient 2', quantity='2 tablespoons')
        ingredient3 = Ingredient.objects.create(name='Ingredient 3', quantity='3 pieces')

        # Associate ingredients with recipes
        RecipeIngredient.objects.create(recipe=recipe1, ingredient=ingredient1)
        RecipeIngredient.objects.create(recipe=recipe1, ingredient=ingredient2)
        RecipeIngredient.objects.create(recipe=recipe2, ingredient=ingredient2)
        RecipeIngredient.objects.create(recipe=recipe2, ingredient=ingredient3)
        RecipeIngredient.objects.create(recipe=recipe3, ingredient=ingredient1)
        RecipeIngredient.objects.create(recipe=recipe3, ingredient=ingredient3)

        # Associate recipes with restaurants
        RestaurantRecipe.objects.create(restaurant=restaurant1, recipe=recipe1)
        RestaurantRecipe.objects.create(restaurant=restaurant1, recipe=recipe2)
        RestaurantRecipe.objects.create(restaurant=restaurant2, recipe=recipe3)
        RestaurantRecipe.objects.create(restaurant=restaurant2, recipe=recipe1)  # Recipe 1 belongs to both restaurants

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with mock data'))
