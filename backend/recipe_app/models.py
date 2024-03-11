from django.db import models

class Restaurant(models.Model):
    """
    Represents a restaurant.
    """
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """
    Represents a recipe.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    """
    Represents an ingredient used in recipes.
    """
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    """
    Represents a many-to-many relationship between recipes and ingredients.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe.title} - {self.ingredient.name}"

class RestaurantRecipe(models.Model):
    """
    Represents a many-to-many relationship between restaurants and recipes.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.restaurant.name} - {self.recipe.title}"
