from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug>/', post, name='post'),
    path('update_article_vote/', updateArticleVote, name='update_article_vote'),
    path('update_comment_vote/', updateCommentVote, name='update_comment_vote'),
    path('update_reply_vote/', updateReplyVote, name='update_reply_vote'),
    path('post/<slug>/add_comment', addComment, name='add_comment'),
    path('add_reply/', addReply, name='add_reply'),
    # path('add_subreply/', addSubReply, name='add_subreply'),
]
