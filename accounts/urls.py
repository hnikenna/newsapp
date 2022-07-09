from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
# import .views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<username>/', get_user_profile, name='profile'),
    path('<username>/edit', get_user_profile_edit, name='edit_profile'),
]
