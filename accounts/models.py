from django.contrib.auth.models import AbstractUser
from newsapp.models import AwardItem
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        try:
            this, created = Profile.objects.get_or_create(user=self)
            # this.avatar.image.add()
            this.save()
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    @property
    def name(self):
        return f'{self.username}'

    @property
    def avatar(self):
        profile = get_object_or_404(Profile, user=self)
        return profile.avatar

    @property
    def is_verified(self):
        profile = get_object_or_404(Profile, user=self)
        return profile.is_verified

    @property
    def awards(self):
        profile = get_object_or_404(Profile, user=self)
        awards = profile.award.all()
        return awards


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    username = models.CharField(blank=True, null=True, max_length=50)
    first_name = models.CharField(blank=True, null=True, max_length=50)
    last_name = models.CharField(blank=True, null=True, max_length=50)
    phone = models.CharField(blank=True, null=True, max_length=16)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=False, default='static_media/user.png')
    award = models.ManyToManyField(AwardItem, blank=True)

    def save(self, *args, **kwargs):
        try:
            # Update username
            self.username = self.user.name
            this = Profile.objects.get(id=self.id)
            if this.avatar != self.avatar and this.avatar != 'static_media/user.png':
                this.avatar.delete(save=False)

            if self.avatar == '':
                self.avatar = 'static_media/user.png'
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.name

    @property
    def fullname(self):
        first = self.first_name if self.first_name else ' '
        last = self.last_name if self.last_name else ' '

        return str(first + ' ' + last)
