"""
Views for the recipe API."""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe.serializers import RecipeSerializer

# ModelVeiwSet is set to specifically work with a model
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializers_class = RecipeSerializer
    # This query represent the objects that are avaialable to
    # this view set.
    queryset = Recipe.objects.all()
    # To use endpoint we need token authentication
    authetication_classes = [TokenAuthentication]
    # Cheking that user was authenticated
    permission_classes = [IsAuthenticated]

    # Over writting the get query method to filter result by
    # only returning user's recipes, instead of all recipes
    def get_queryset(self):
        """Retrieve recipes for authentication user."""
        # The order_by('-id') will filter to retunr user's recipes
        return self.queryset.filter(user=self.request.user).order_by('-id')




