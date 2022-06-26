from.models import VoteItem
from django.dispatch import receiver
from django.db.models.signals import pre_delete


def delete_votes(Post, type='c'):

    @receiver(post_delete, sender=Post)
    def remove_vote_item(sender, instance, **kwargs):
        votes = VoteItem.objects.filter(parent=type, parent_id=instance.id)
        for vote in votes:
            vote.delete()
        