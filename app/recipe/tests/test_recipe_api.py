from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')

# Helper function for creating recipe
def create_recipe(user, **params):
    """"Create and return a sample reciple."""
    # Default for a recipe. We can overwrite them, if
    # we need to use them for a test.
    defaults = {
        'title' : 'Sample recipe title',
        'time_minutes' : 22,
        'price' : Decimal('5.25'),
        'description' : 'Sample description',
        'link' : 'http://example.com/recipe.pdf'

    }
    # Params contains parameters passed by the user. This line
    # will over write default values with input provided by the user.
    defaults.update(params)

    # Creating our recipe
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

class PublicRecipeAPITest(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):
    """Test authenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipe(self):
        """Test retriving a recipe list"""

        # Adding 2 recipes to database
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        # Getting our list of recipes
        res = self.client.get(RECIPE_URL)
        # Getting recipes added, order by most recent
        recipe = Recipe.objects.all().order_by('-id')
        # Expect serializer to match the response
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Making sure data from serializer and res match
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated users."""
        user2 = get_user_model().objects.create_user(
            'user2@example.com',
            'newpass123',
        )

        # Adding 2 recipes by two different user
        create_recipe(user=user2)
        create_recipe(user=self.user)

        # Getting the list of all recipes recipes
        res = self.client.get(RECIPE_URL)

        # Getting recipes created by self.user
        recipe = Recipe.objects.filter(user=self.user)
        # Expect serializer to match the response self.user
        serializer = RecipeSerializer(recipe, many=True)
        # Checking for success code
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Checking that res and serializer match (do not include data)
        # for user2
        self.assertEqual(res.data, serializer.data)

