from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

import dectauth.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            URLRouter(
                dectauth.routing.websocket_urlpatterns
            )
        )
    ),
})
