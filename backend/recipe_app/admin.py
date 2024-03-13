from django.contrib import admin
from .models import Restaurant, Recipe, Ingredient, RecipeIngredient, RestaurantRecipe

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')

class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')

class RestaurantRecipeAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'recipe')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RestaurantRecipe, RestaurantRecipeAdmin)
