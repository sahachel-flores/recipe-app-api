"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    # creates a new user everytime this method is called.
    # PW field is set to None in case we want to create an unusable
    # user. We can also add extra fields if we want
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        # calling the self.mode is the same as declaring a new
        # User object, because the UserManager manages User class.
        # The we pass the email through the normalize_email method
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # Set encrypted password. Can not view password in db
        user.set_password(password)
        # Saves the user model. using=self._db support adding multiple db
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create and return a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Base User class from AbstractBaseUser, PermissionsMixin
# Abs..User Class contains functionality for auth system
# Per..Mixin Class contains functionality for permission system
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    # using emailField provided by django to to validate email
    # max_length set to max value, and want unique emails
    email = models.EmailField(max_length=255, unique=True)
    # using character field provided by django
    name = models.CharField(max_length=255)
    # is_active define that users who register will be active by default
    is_active = models.BooleanField(default=True)
    # variable determine is user can login with djando admin, false by default
    is_staff = models.BooleanField(default=False)

    # Assgining userManager to user class
    objects = UserManager()

    #filed for authentication
    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe Object."""
    # Stored the user. Using ForeigKey because it allows us
    # to set up a relationship between this recipe model and
    # another model.
    user = models.ForeignKey(
        # passing the AUTH model we defined in our setting.py file
        settings.AUTH_USER_MODEL,
        # if related object is deleted, we are also cancating this
        # change to the model. Ex delete user -> we delete its recipes too
        on_delete=models.CASCADE,
    )

    # Populating the object's fieldss
    title=models.CharField(max_length=255)
    # Textfild is desiged to hold more data
    # CharField is faster
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255,blank=True)

    # The special method to return the string representation of this object
    def __str__(self) -> str:
        return self.title


