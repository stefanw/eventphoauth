from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .api import get_challenge, heartbeat_challenge


class ChallengeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        url_route = self.scope['url_route']
        self.challenge_uuid = url_route['kwargs']['challenge_uuid']
        self.challenge = await get_challenge(self.challenge_uuid)
        if self.challenge is None:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.challenge_uuid,
            self.channel_name
        )
        await self.accept()
        await heartbeat_challenge(self.challenge_uuid)

    async def disconnect(self, close_code):
        # Leave room group
        if self.challenge is not None:
            await self.channel_layer.group_discard(
                self.challenge_uuid,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive_json(self, content):
        if content['type'] == 'hearbeat':
            await heartbeat_challenge(self.challenge_uuid)
            return

    async def solved(self, event):
        await self.send_json({
            'type': 'solved'
        })
