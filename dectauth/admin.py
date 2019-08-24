from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.conf.urls import url
from django.utils.html import format_html

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from .models import Challenge


class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'key', 'created', 'last_seen', 'solved',
        'mark_solved_button'
    )
    list_filter = ('solved',)
    search_fields = ('username',)
    actions = ['solve_challenge']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<obj_id>.+)/mark-solved/$',
                self.admin_site.admin_view(self.mark_solved),
                name='dectauth-challenge-mark_solved',
            ),
        ]
        return custom_urls + urls

    def solve_challenge(self, request, queryset):
        channel_layer = get_channel_layer()
        queryset.update(solved=True, last_seen=timezone.now())
        for challenge in queryset:
            async_to_sync(channel_layer.group_send)(
                str(challenge.uuid), {"type": "solved"}
            )

    def mark_solved_button(self, obj):
        if obj.solved:
            return ''
        return format_html(
            '<button class="button" data-solvechallenge="{}">Mark solved</button>',
            reverse('admin:dectauth-challenge-mark_solved', args=[obj.pk])
        )
    mark_solved_button.short_description = 'Mark solved'
    mark_solved_button.allow_tags = True

    def mark_solved(self, request, obj_id, *args, **kwargs):
        if request.method != 'POST':
            return
        self.solve_challenge(request, Challenge.objects.filter(id=obj_id))
        self.message_user(request, 'Success')
        return HttpResponse()


admin.site.register(Challenge, ChallengeAdmin)
