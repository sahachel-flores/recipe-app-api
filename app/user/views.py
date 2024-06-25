"""
Views for the user API
"""
# Handle the logic for create object in the database.
# Does that by providing a bunch of different base classes
# that we can configure for our views. Also give us the
# option of overwritting behavio.
from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# Serializer we created
from user.serializers import(
    UserSerializer,
    AuthTokenSerializer,
)

# CreateAPIView handle post request (creating obj in db)
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # Above base class requires a serialize. We use the
    # serializer we created.
    serializer_class = UserSerializer

    # Connecting URL to the view

# This classe is based of ObtainAuthToken
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    # Custom serializer class we create.
    # Recall that default uses username and our uses email
    serializer_class = AuthTokenSerializer
    # Optional: it uses the default render of classes for
    # this obtain or token view
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    # Set user serializer
    serializer_class = UserSerializer
    # Set authent. using token auth
    authentication_classes = [authentication.TokenAuthentication]
    # Set the user's permission: user must be authenticated
    permission_classes = [permissions.IsAuthenticated]

    # Overwriting the get function, we just retrieve the user object
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user