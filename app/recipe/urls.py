"""
URL mapping for the recipe app.
"""
from django.urls import (
    path,
    include,
)
# Use default router w/ API view to automatically create
# routes for all the different options available for that view
from rest_framework.routers import DefaultRouter
# Importing view file we created
from recipe import views

# Creating router
router  = DefaultRouter()
# Registering viewset with default router. This create a new
# endpoint API/recipe and assigns all the view.RecipeViewSet
# endpoints that end point
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns  = [
    path('', include(router.urls)),
]