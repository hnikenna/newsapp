from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Profile


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def get_user_profile(request, username):
    user = Profile.objects.get(username=username)
    return render(request, 'profile.html', {"duser":user})


def get_user_profile_edit(request, username):
    user = Profile.objects.get(username=username)
    return render(request, 'edit_profile.html', {"duser":user})
