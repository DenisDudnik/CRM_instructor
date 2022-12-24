import asyncio

import websockets
from websockets.legacy.server import WebSocketServerProtocol


class WebsocketHandler:

    CONNECTED = {}

    async def __call__(self, ws: WebSocketServerProtocol, *args, **kwargs):
        pass


async def main():
    print("server start")
    async with websockets.serve(WebsocketHandler(), "", 8181):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
