# from django.forms import ModelForm, Textarea, HiddenInput, CharField
# from .models import Comment, Article
from django import forms


class CommentForm(forms.Form):
    # name = forms.CharField()
    content = forms.CharField()


class ReplyForm(forms.Form):
    recipent = forms.CharField()
    comment = forms.CharField()
    content = forms.CharField()
