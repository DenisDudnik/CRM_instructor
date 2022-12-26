import asyncio
from collections import deque

import websockets
from asgiref.sync import sync_to_async
from websockets.legacy.server import WebSocketServerProtocol

from users.models import UserMessage
from websocket_server.schema import WebsocketData


class WebsocketHandler:

    CONNECTED = {}
    actions = deque()

    @staticmethod
    async def send(data: WebsocketData, ws: WebSocketServerProtocol):
        try:
            await ws.send(data.json())
        except websockets.ConnectionClosed:
            pass

    async def init(self, data: WebsocketData, **kwargs):
        ws: WebSocketServerProtocol = kwargs.get('socket')
        self.__class__.CONNECTED[data.from_user] = ws

    async def message(self, data: WebsocketData, **kwargs):
        ws: WebSocketServerProtocol = self.CONNECTED.get(data.to_user)
        await sync_to_async(UserMessage.objects.create, thread_sensitive=True)(
            kind='msg',
            from_user_id=data.from_user,
            to_user_id=data.to_user,
            text=data.text
        )
        if ws is not None:
            await ws.send(data.json())

    async def __call__(self, ws: WebSocketServerProtocol, *args, **kwargs):
        async for msg in ws:
            data = WebsocketData.parse_raw(msg)
            handler = getattr(self, data.kind.value)
            await handler(data, socket=ws)


async def main():
    print("server start")
    async with websockets.serve(WebsocketHandler(), "", 8181):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
