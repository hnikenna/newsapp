from django.contrib.auth.models import AbstractUser
from newsapp.models import AwardItem
from django.db import models
from django.shortcuts import get_object_or_404


class CustomUser(AbstractUser):
    first_name = models.CharField(blank=True, null=True, max_length=50)
    last_name = models.CharField(blank=True, null=True, max_length=50)
    phone = models.CharField(blank=True, null=True, max_length=16)

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
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=False, default='static_media/user.png')
    award = models.ManyToManyField(AwardItem, blank=True)

    def save(self, *args, **kwargs):
        try:
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
