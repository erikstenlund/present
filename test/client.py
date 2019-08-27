#!/usr/bin/env python

# WS client example

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            name = input("> ")
            await websocket.send(name)

asyncio.get_event_loop().run_until_complete(hello())

