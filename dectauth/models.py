import uuid
from random import SystemRandom

from django.db import models
from django.urls import reverse
from django.utils import timezone

KEY_LENGTH = 6


class ChallengeManager(models.Manager):
    def create_challenge(self, **kwargs):
        cryptogen = SystemRandom()
        return Challenge.objects.create(
            key=str(cryptogen.randrange(10 ** KEY_LENGTH)).zfill(KEY_LENGTH),
            **kwargs
        )


class Challenge(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_seen = models.DateTimeField(default=timezone.now, editable=False)
    key = models.CharField(max_length=10, editable=False)
    solved = models.BooleanField(default=False)
    state = models.TextField(blank=True)
    username = models.CharField(max_length=255, blank=True)

    objects = ChallengeManager()

    class Meta:
        verbose_name = 'Challenge'
        verbose_name_plural = 'Challenges'
        ordering = ('-created',)

    def __str__(self):
        return '{username}: {key}'.format(username=self.username, key=self.key)

    def get_absolute_url(self):
        return reverse('dectauth:challenge', kwargs={
            'challenge_uuid': str(self.uuid)
        })
