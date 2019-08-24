from django.utils import timezone

from channels.db import database_sync_to_async

from .models import Challenge


@database_sync_to_async
def get_challenge(challenge_uuid):
    try:
        return Challenge.objects.get(uuid=challenge_uuid)
    except Challenge.DoesNotExist:
        return None


@database_sync_to_async
def heartbeat_challenge(challenge_uuid):
    Challenge.objects.filter(uuid=challenge_uuid).update(
        last_seen=timezone.now()
    )


@database_sync_to_async
def solve_challenge(challenge_uuid):
    Challenge.objects.filter(uuid=challenge_uuid).update(
        solved=True
    )
