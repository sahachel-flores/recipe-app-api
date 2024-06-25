"""
Serializers for the user API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
# library that include tool for serializer
from rest_framework import serializers


# Class based of the model serializer. Allows to automatically
# validate and save things to a specific mode that we define in
# our serializer
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object. Serializer is a way to convert
    objects to and from python objects.
    Takes adjecent input from the API & validates the input to make
    sure that it's secure and correct. Then conver it to python object
    or database model.
    """
    # This class is where we tell djange the models, fields, and additional
    # arguments we want to pass to serilizer
    class Meta:
        # Get user model
        model = get_user_model()
        # Fields that should be part of the model. Only include feels that
        # the user will be allow to change through API
        fields = ['email', 'password', 'name']
        # User can write value, but can not view them (write only).
        # If user passes in a value less than minimum, we through 400 bad
        # request response.
        extra_kwargs = {'password':{'write_only': True, 'min_length':5}}

        # This function allow us to over write behavior of the serializer when
        # new objects are created.
        # Default behavior: Create object w/ whatever values are passed in
        # New behavior: Use the create user function that we created.
    def create(self, validated_data):
        """Create and retunr a user with encrypted password"""
        # overwrite of the create models.
        # Function will run after validation
        return get_user_model().objects.create_user(**validated_data)


    def update(self, instance, validated_data):
        """Update and return user."""
        # Getting new password
        password = validated_data.pop('password', None)
        # Updating the password
        user = super().update(instance, validated_data)
        # Checking if password was set
        if password:
            user.set_password(password)
            user.save()
        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the auth token"""
    email=serializers.EmailField()
    password=serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validates and authenticate the user."""
        # Getting user info
        email = attrs.get('email')
        password = attrs.get('password')
        # Checking if user username and password exist
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        # Raising error message if user was not auth.
        if not user:
            msg=_('unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        # Set user, we were able to auth. and return attibutes
        attrs['user'] = user
        return attrs
