#!/usr/bin/env python

import pyqrcode
import asyncio
import websockets

class Message:
    def __init__(self, message: str):
        self.valid = False
        self.token = ''
        self.command = ''

        if ':' in message:
            [self.token, self.command] = message.split(':')
            self.valid = self.token != '' and self.command != ''

    def GetToken(self) -> str:
        return self.token

    def GetCommand(self) -> str:
        return self.command

    def IsValid(self) -> bool:
        return self.valid

def ForwardHandler():
    print('Called app forward handler')
    
def BackHandler():
    print('Called app back handler')

def CheckToken(func):
    def wrapper(message) -> Message:
        if message and message.token == 'secret':
            return func(message)
        else:
            return func(None)
    return wrapper

def CheckMessage(func):
    def wrapper(message) -> Message:
        if message and message.IsValid():
            return func(message)
        else:
            return func(None)
    return wrapper

@CheckToken
@CheckMessage
async def HandleCommand(message):
    if message is None:
        return False

    handlers = {
        'forward' : ForwardHandler,
        'back' : BackHandler
    }

    if message.command in handlers:
        handlers[message.command]()

    return True

async def CommandSocket(websocket, path):
    async for message in websocket:
        await HandleCommand(Message(message))

if __name__ == "__main__":
    host = 'localhost'
    port = 8765
    token = 'secret'

    url = 'ws://%s:%d/%s' % (host, port, token)
    qr = pyqrcode.create(url)

    print(url)
    print(qr.terminal(quiet_zone=1))

    server = websockets.serve(CommandSocket, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

