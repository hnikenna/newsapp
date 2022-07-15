from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email",)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email",)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'bio']
        # fields = '__all_  _'


class SocialsEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['website', 'tiktok', 'twitter', 'instagram', 'facebook']
        # fields = '__all_  _'


class AvatarUploadForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['avatar']
