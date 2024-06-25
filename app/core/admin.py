"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Integrates with the django translation system. (Will not implement
# translation for this project). But it's a best practice to have it.
from django.utils.translation import gettext_lazy as _
from core import models

# Creating new UserAdmin Class base of the deault UserAdmin class.
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    # Order admin users by id
    ordering = ['id']

    # Display email and name in the list display
    list_display = ['email', 'name']

    # None placeholder means not title.
    # Rest of the code custimize the fildsets class variables.
    # We only specify fields that exits in our model.
    fieldsets = (
        (None , {'fields':('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('important dates'),
            {
                'fields':('last_login',)
            }
        ),
    )
    readonly_fields = ['last_login']

    # The classes key allows us to add custum css classes in Django.
    # Documentation explaions that adding the 'wide' makes the page
    # looks neat and tidier.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':(
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

# Register your user model. Adding the UserAdmin field
# is optional. However, W/out it, we would not use
# the default userAdmin.
# We want to use the UserAdmin we created above.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)