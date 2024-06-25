"""
URL mappings for the user API.
"""

from django.urls import path

from user import views

#
app_name = 'user'

# Endpoint 'create' will be handdle by the CrateUserView class
# that we created. Other end points follow the same logic.
urlpatterns = [
    # Note: djnago expects a natural function for class parameter,
    # reason for using the as_view().
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]