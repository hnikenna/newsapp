from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from newsapp.models import AwardItem
from news_project.utils import *


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
        # awards = AwardItem.objects.filter(owner=self)
        awards = AwardItem.objects.filter(owner=self, parent_id=None)
        # awards2 = AwardItem.objects.all()
        # for award in awards2:
        #     print(type(award.parent_id))
        #     print(award.parent_id is None)
        return awards

    @property
    def awards_received(self):
        awards = AwardItem.objects.filter(owner=self)
        awards2 = []
        for award in awards:
            if award.parent_id is not None:
                awards2.append(award)
            # print(award.parent_id is None)
        return awards2

    @property
    def exchangeval(self):
        awards = AwardItem.objects.filter(owner=self)
        awards2 = 0
        # awards2 = {}
        for award in awards:
            if award.parent_id is not None:
                awards2 += (award.award.price * award.quantity) / 5

        awards2 = format_currency(awards2)
        return awards2


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    username = models.CharField(blank=True, null=True, max_length=50)
    full_name = models.CharField(blank=True, null=True, max_length=100)
    phone = models.CharField(blank=True, null=True, max_length=16)
    bio = models.TextField(blank=True, null=True, max_length=250)
    website = models.CharField(blank=True, null=True, max_length=100)
    facebook = models.CharField(blank=True, null=True, max_length=50)
    twitter = models.CharField(blank=True, null=True, max_length=50)
    instagram= models.CharField(blank=True, null=True, max_length=50)
    tiktok = models.CharField(blank=True, null=True, max_length=50)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=False, default='static_media/user.png')
    # award = models.ManyToManyField(AwardItem, blank=True)

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
