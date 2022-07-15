from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(VoteItem)
admin.site.register(Award)
admin.site.register(AwardTransaction)
admin.site.register(AwardItem)
