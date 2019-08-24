from django.conf.urls import url

from oauth2_provider.views import (
    AuthorizationView, TokenView,
)
from .api_views import ProfileView
from .views import start, challenge


app_name = 'dectauth'

urlpatterns = [
    url(r'^$', start, name="start"),
    url(r'^api/user/', ProfileView.as_view(), name='api-user-profile'),
    url(r'^challenge/(?P<challenge_uuid>[^/]+)/$', challenge, name='challenge'),
    url(r'^authorize/$', AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', TokenView.as_view(), name="token"),
]
