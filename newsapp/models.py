import datetime

from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from .utils import breadcrumb
# from django.contrib.auth import get_user_model


# Create your models here.
class Award(models.Model):

    ROTATE = 'rotate'
    GLOW = 'glow'
    SHAKE = 'shake'

    ANIMATION_CHOICES = [
        (ROTATE, 'Rotate'),
        (GLOW, 'Glow'),
        (SHAKE, 'Shake'),
    ]
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=20)
    animation = models.CharField(choices=ANIMATION_CHOICES, blank=True, max_length=50)
    price = models.IntegerField(default='500')

    def __str__(self):
        return self.name


class AwardItem(models.Model):

    award = models.ForeignKey(Award, on_delete=models.PROTECT)
    award_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.award_quantity) + ' - ' + self.award.name


class Reply(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # respondee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    yes_vote = models.IntegerField(default=0)
    no_vote = models.IntegerField(default=0)
    award = models.ManyToManyField(AwardItem, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username + ' - ' + str(self.content[:100])

    @property
    def awards(self):
        awards = self.award.all()
        # print(awards)
        return awards

    @property
    def time_ago(self):
        start_time = self.date
        now_time = datetime.now(timezone.utc)

        difference = int((now_time - start_time).total_seconds())

        second = [1, 'seconds']
        minute = [60, 'minutes']
        hour = [60 * minute[0], 'hours']
        day = [24 * hour[0], 'days']
        week = [7 * day[0], 'weeks']
        month = [4 * week[0], 'months']
        year = [12 * month[0], 'years']

        times = [year, month, week, day, hour, minute, second]
        for time in times:
            if difference >= time[0]:
                time_ago = int(difference / time[0])
                if time_ago <= 1:
                    timeframe = time[1].rstrip('s')
                else:
                    timeframe = time[1]

                timeitem = str(time_ago) + ' ' + timeframe + ' ago'
                return timeitem
        return 'Just Now'

    @property
    def is_award(self):
        awards = self.award.all()
        # print('Awards:', len(awards))
        if len(awards) <= 0:
            return False
        return True
    
    @property
    def get_votes(self):
        votes = VoteItem.objects.filter(parent='r', parent_id=self.id)
        return votes


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    yes_vote = models.IntegerField(default=0)
    no_vote = models.IntegerField(default=0)
    award = models.ManyToManyField(AwardItem, blank=True)
    # reply = models.ManyToManyField('self', null=True, blank=True)
    reply = models.ManyToManyField(Reply, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    # voter = models.F

    def __str__(self):
        return self.author.username + ' - ' + str(self.content[:30])

    @property
    def awards(self):
        awards = self.award.all()
        # print(awards)
        return awards

    @property
    def time_ago(self):
        start_time = self.date
        now_time = datetime.now(timezone.utc)

        difference = int((now_time - start_time).total_seconds())

        second = [1, 'seconds']
        minute = [60, 'minutes']
        hour = [60 * minute[0], 'hours']
        day = [24 * hour[0], 'days']
        week = [7 * day[0], 'weeks']
        month = [4 * week[0], 'months']
        year = [12 * month[0], 'years']

        times = [year, month, week, day, hour, minute, second]
        for time in times:
            if difference >= time[0]:
                time_ago = int(difference / time[0])
                if time_ago <= 1:
                    timeframe = time[1].rstrip('s')
                else:
                    timeframe = time[1]

                time_item = str(time_ago) + ' ' + timeframe + ' ago'
                return time_item
        return 'Just Now'

    @property
    def replies(self):
        try:
            replies = self.reply.all()
            return replies
        except:
            return 'No Comment!'

    @property
    def is_award(self):
        awards = self.award.all()
        # print('Awards:', len(awards))
        if len(awards) == 0:
            return False
        return True

    @property
    def get_votes(self):
        votes = VoteItem.objects.filter(parent='c', parent_id=self.id)
        return votes


class Article(models.Model):
    title = models.CharField(max_length=250)
    header_text = models.CharField(max_length=250, blank=True)
    content = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, null=False, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    is_draft = models.BooleanField(default=True)
    image = models.ImageField(upload_to='articles', blank=True)
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=200)
    # tags = models.CharField(max_length=250)
    yes_vote = models.IntegerField(default=0)
    no_vote = models.IntegerField(default=0)
    comment = models.ManyToManyField(Comment, blank=True)
    # voter = models.ManyToManyField

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.title = str(self.title.title())
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})

    @property
    def get_title(self):
        return breadcrumb(self.title, 70)

    @property
    def get_short_title(self):
        return breadcrumb(self.title, 50)

    @property
    def get_mid_content(self):
        return breadcrumb(self.content, 2500)

    @property
    def get_short_content(self):
        return breadcrumb(self.content, 200)

    @property
    def get_shorter_content(self):
        return breadcrumb(self.content, 100)

    @property
    def username(self):
        return str(self.author.username).title()

    @property
    def comments(self):
        try:
            comments = self.comment.all()
            return comments
        except:
            return 'No Comment!'

    @property
    def get_votes(self):
        votes = VoteItem.objects.filter(parent='a', parent_id=self.id)
        return votes

    @property
    def time_ago(self):
        start_time = self.date
        now_time = datetime.date(datetime.now(timezone.utc))

        difference = int((now_time - start_time).total_seconds())

        second = [1, 'seconds']
        minute = [60, 'minutes']
        hour = [60 * minute[0], 'hours']
        day = [24 * hour[0], 'days']
        week = [7 * day[0], 'weeks']
        month = [4 * week[0], 'months']
        year = [12 * month[0], 'years']

        times = [year, month, week, day, hour, minute, second]
        for time in times:
            if difference >= time[0]:
                time_ago = int(difference / time[0])
                if time_ago <= 1:
                    timeframe = time[1].rstrip('s')
                else:
                    timeframe = time[1]

                timeitem = str(time_ago) + ' ' + timeframe + ' ago'
                return timeitem
        return 'Just Now'


class VoteItem(models.Model):
    PARENT_TYPES = [('a', 'Article'), ('c', 'Comment'), ('r', 'Reply')]
    POLL_CHOICE = [('yes', 'Yes'), ('no', 'No')]
    parent = models.CharField(max_length=1, choices=PARENT_TYPES)
    parent_id = models.PositiveIntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.CharField(max_length=3, choices=POLL_CHOICE, blank=True)

    def __str__(self):
        return self.parent + ' - ' + self.voter.username
