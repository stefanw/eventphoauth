from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer


def create_user_and_login(request, challenge):
    user, created = User.objects.get_or_create(
        username=challenge.username,
        email='',
        defaults={}
    )
    user.set_unusable_password()
    user.save()
    login(request, user)
    return user


def notify_solved(challenge):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        str(challenge.uuid), {"type": "solved"}
    )


def solve_challenge(challenge):
    challenge.solved = True
    challenge.last_seen = timezone.now()
    challenge.save()
    notify_solved(challenge)
