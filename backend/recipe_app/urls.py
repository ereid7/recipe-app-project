from django.contrib import admin
from django.urls import include, path

import django_js_reverse.views
from common.routes import routes as common_routes
from rest_framework.routers import DefaultRouter

from recipe_app.views import RecipeView, RecipeListView, ScrapeRecipeView, RestaurantListView

router = DefaultRouter()

routes = common_routes
for route in routes:
    router.register(route["regex"], route["viewset"], basename=route["basename"])

urlpatterns = [
    path("", include("common.urls"), name="common"),
    path("admin/", admin.site.urls, name="admin"),
    path("admin/defender/", include("defender.urls")),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path("api/", include(router.urls), name="api"),
    path("api/recipes/<int:pk>/", RecipeView.as_view(), name="recipe_detail"),
    path("api/recipes/", RecipeListView.as_view(), name="recipe_list"),
    path("api/scrape-recipe/", ScrapeRecipeView.as_view(), name="scrape_recipe"),
    path('api/restaurants/', RestaurantListView.as_view(), name='restaurant_list'),
]
