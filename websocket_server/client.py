import asyncio
from threading import Thread

import websockets

from websocket_server.schema import WebsocketData


async def notify(data: WebsocketData):
    async with websockets.connect('ws://localhost:8181') as ws:
        await ws.send(data.json())


def send_notification(data: WebsocketData):
    thread = Thread(target=asyncio.run, args=[notify(data)], daemon=True)
    thread.start()
    thread.join(timeout=1)
