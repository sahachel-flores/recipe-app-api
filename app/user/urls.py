"""
URL mapping for the user API.
"""

from django.urls import path

from user import views

#
app_name = 'user'

# Call that go through the 'create' will be handdle by the
# CrateUserView class that we created
# Note: djnago expexts a natural function for class parameter,
# reason for using the as_view().
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]