import json
import random

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


# Create your views here.
class HomeView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'all_article_list'


def post(request, slug):
    user = request.user
    article = get_object_or_404(Article, slug=slug)
    all_awards = Award.objects.all()
    # all_articles = Article.objects.all()[:4]
    featured = Article.objects.all()[:3]
    # featured = random.choices(all_articles, weights=None, cum_weights=None, k=4)

    # Code to display user article choices on page
    articleVoteItems = article.get_votes
    article.selectYV = ''
    article.selectNV = ''

    for vi in articleVoteItems:
        if user.username == vi.voter.username:
            if vi.choice == 'yes':
                article.selectYV = 'selected'
            elif vi.choice == 'no':
                article.selectNV = 'selected'

    comments = article.comment.all()
    for comment in comments:
        contentbox = str(comment.content).split('\n')
        awards = comment.awards
        for awarditem in awards:
            pass

    context = {'article': article, 'all_awards': all_awards, 'featured': featured}
    return render(request, 'post_single.html', context)


@csrf_exempt
def updateArticleVote(request):
    user = request.user
    data = json.loads(request.body)
    slug = data['Slug']
    poll = data['Poll']

    article = Article.objects.get(slug=slug)

    def response():
        return JsonResponse('ArticleVote was updated!!', safe=False)
        # return JsonResponse({'y': article.yes_vote, 'n': article.no_vote})

    # if user is guest:
    if not user.is_authenticated:
        return JsonResponse('User is guest', safe=False)

    vote, created = VoteItem.objects.get_or_create(voter=user, parent='a', parent_id=article.id, article=article)

    # Add code to allow only one vote per user
    if created or vote.choice == '':

        if poll == 'yes':
            article.yes_vote += 1
            vote.choice = 'yes'
        elif poll == 'no':
            article.no_vote += 1
            vote.choice = 'no'

        article.save()
        vote.save()

        return response()

    else:
        if poll == vote.choice:

            # Remove Vote
            if poll == 'no':
                article.no_vote -= 1
                vote.choice = ''
            else:
                article.yes_vote -= 1
                vote.choice = ''

            article.save()
            vote.save()

            return response()

        elif poll == 'no':
            article.no_vote += 1
            article.yes_vote -= 1
            vote.choice = 'no'

        elif poll == 'yes':
            article.no_vote -= 1
            article.yes_vote += 1
            vote.choice = 'yes'

        article.save()
        vote.save()

        return response()


@csrf_exempt
def updateCommentVote(request):
    user = request.user
    data = json.loads(request.body)
    slug = data['Slug']
    poll = data['Poll']
    id = data['ID']

    article = get_object_or_404(Article, slug=slug)
    comment = get_object_or_404(article.comments, id=id)

    # Handle guest users:
    if not user.is_authenticated:
        return JsonResponse('User is guest', safe=False)

    vote, created = VoteItem.objects.get_or_create(voter=user, parent='c', parent_id=comment.id, comment=comment)
    print(vote.choice)

    if created or vote.choice == '':
        if poll == 'yes':
            comment.yes_vote += 1
            vote.choice = 'yes'
        elif poll == 'no':
            comment.no_vote += 1
            vote.choice = 'no'

        comment.save()
        vote.save()
        return JsonResponse('CommentVote was updated!', safe=False)

    else:
        if poll == vote.choice:

            # Remove Vote
            if poll == 'no':
                comment.no_vote -= 1
                vote.choice = ''
            else:
                comment.yes_vote -= 1
                vote.choice = ''

            comment.save()
            vote.save()
            return JsonResponse('CommentVote is removed', safe=False)

        elif poll == 'no':
            comment.no_vote += 1
            comment.yes_vote -= 1
            vote.choice = 'no'

        elif poll == 'yes':
            comment.no_vote -= 1
            comment.yes_vote += 1
            vote.choice = 'yes'

        comment.save()
        vote.save()
        return JsonResponse(f'CommentVote was updated', safe=False)


@csrf_exempt
def updateReplyVote(request):
    user = request.user
    data = json.loads(request.body)
    slug = data['Slug']
    poll = data['Poll']
    comment_id = data['Comment ID']
    id = data['ID']

    article = get_object_or_404(Article, slug=slug)
    comment = get_object_or_404(article.comments, id=comment_id)
    reply = get_object_or_404(comment.replies, id=id)

    # if user is guest:
    if not user.is_authenticated:
        return JsonResponse('User is guest', safe=False)

    vote, created = VoteItem.objects.get_or_create(voter=user, parent='r', parent_id=reply.id, reply=reply)

    if created or vote.choice == '':

        if poll == 'yes':
            reply.yes_vote += 1
            vote.choice = 'yes'
        elif poll == 'no':
            reply.no_vote += 1
            vote.choice = 'no'

        reply.save()
        vote.save()
        return JsonResponse('Reply-Vote was updated!', safe=False)

    else:
        if poll == vote.choice:

            # Remove Vote
            if poll == 'no':
                reply.no_vote -= 1
                vote.choice = ''
            else:
                reply.yes_vote -= 1
                vote.choice = ''

            reply.save()
            vote.save()
            return JsonResponse('ReplyVote is removed', safe=False)

        elif poll == 'no':
            reply.no_vote += 1
            reply.yes_vote -= 1
            vote.choice = 'no'

        elif poll == 'yes':
            reply.no_vote -= 1
            reply.yes_vote += 1
            vote.choice = 'yes'

        reply.save()
        vote.save()
        return JsonResponse('Reply-Vote was updated!', safe=False)


def addComment(request, slug):
    form = CommentForm(request.POST)
    user = request.user

    # if user is guest:
    if not user.is_authenticated:
        return JsonResponse('User is guest', safe=False)
        # return HttpResponse("<script>alerT(e, 'Oops! You have to be logged in to vote', '#C94B0C');</script>")

    if form.is_valid():
        data = form.cleaned_data
        content = data['content']
        article = get_object_or_404(Article, slug=slug)
        comment = Comment(author=user, content=content)
        comment.yes_vote += 1
        comment.save()

        # Add user vote as an upvote
        voteitem = VoteItem(voter=user, parent='c', parent_id=comment.id, comment=comment, choice='yes')
        voteitem.save()
        article.comment.add(comment)
        article.save()

    else:
        print('Form ain\'t valid')
        return JsonResponse('Form ain\'t valid', safe=False)

    # return JsonResponse('Comment Received', safe=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # return HttpResponseRedirect(f'/post/{slug}')
    # return HttpResponse('<script>location.replace(document.referrer);</script>')


def addReply(request):
    form = ReplyForm(request.POST)
    user = request.user

    # if user is guest:
    if not user.is_authenticated:
        return JsonResponse('User is guest', safe=False)

    if form.is_valid():
        data = form.cleaned_data
        print(data)
        content = data['content']
        recipent = data['recipent']
        # verified_img = '<img src="/static/img/verify.png" class="verified text-center">'
        content = f"<span style='color: #3932be'>@{recipent}</span> {content}"
        comment = data['comment']
        comment = get_object_or_404(Comment, id=comment)
        reply = Reply(author=user, content=content)
        reply.yes_vote += 1
        reply.save()
        comment.reply.add(reply)
        comment.save()

        # Add user vote as an upvote
        voteitem = VoteItem(voter=user, parent='r', parent_id=reply.id, reply=reply, choice='yes')
        voteitem.save()
        print('Sub-Reply Added')


    else:
        print('Form ain\'t valid')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
