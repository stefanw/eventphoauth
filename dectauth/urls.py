from django.conf.urls import url

from oauth2_provider.views import (
    AuthorizationView, TokenView,
)
from .api_views import ProfileView
from .views import start, challenge
from .callout_views import challenge_voice_response, challenge_gather_input

app_name = 'dectauth'

urlpatterns = [
    url(r'^$', start, name="start"),
    url(r'^api/user/', ProfileView.as_view(), name='api-user-profile'),
    url(r'^challenge/(?P<challenge_uuid>[^/]+)/$', challenge, name='challenge'),
    url(r'^authorize/$', AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', TokenView.as_view(), name="token"),

    url(r'^callout/(?P<challenge_uuid>[^/]+)/$', challenge_voice_response,
        name='challenge-callout'),
    url(r'^callout-gather/(?P<challenge_uuid>[^/]+)/$', challenge_gather_input,
        name='challenge-callout-gather'),
]
