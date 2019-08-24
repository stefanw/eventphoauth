from django.contrib import admin
from django.utils import timezone

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from .models import Challenge


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('username', 'key', 'created', 'last_seen', 'solved')
    list_filter = ('solved',)
    search_fields = ('username',)
    actions = ['solve_challenge']

    def solve_challenge(self, request, queryset):
        channel_layer = get_channel_layer()
        queryset.update(solved=True, last_seen=timezone.now())
        for challenge in queryset:
            async_to_sync(channel_layer.group_send)(
                str(challenge.uuid), {"type": "solved"}
            )


admin.site.register(Challenge, ChallengeAdmin)
