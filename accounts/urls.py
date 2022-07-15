from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
# import .views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<username>/', get_user_profile, name='profile'),
    path('<username>/edit', edit_user_profile, name='edit_profile'),
    path('<username>/social_edit', edit_user_social, name='edit_social'),
]
