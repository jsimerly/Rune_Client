from __future__ import annotations
import asyncio
import websockets
from typing import Callable
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user.user import User

class NetworkManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NetworkManager, cls).__new__(cls)
            cls._instance.init(*args, **kwargs)
        return cls._instance
    
    def init(self) -> None:
        self.uri = 'ws://localhost:8765'
        self.loop = asyncio.get_event_loop()
        self.websocket = None
        self.message_callback = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        await self.start_listening()

    async def close_connection(self):
        if self.websocket:
            await self.websocket.close()

    def create_task(self, task: Callable):
        self.loop.create_task(task)

    def run_one(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    def login(self, username: str):
        self.create_task(self._login(username))

    async def _login(self, username:str):
        await self.connect()
        package = json.dumps(
            {'username' : username}
        )
        await self.websocket.send(package)

    def send_message(self, user: User, type: str, serialized_message: str):
        self.create_task(self._send_message(user, type, serialized_message))

    async def _send_message(self, user: User, type: str, message: dict):
        if not isinstance(message, dict):
            raise ValueError('Messages must in a dictionry or json format to be sent using send_data.')
        
        if not self.websocket:
            await self.connect()

            package = {
            'type': type,
            'user': user.serialize(),
            'data': message,
        }
        package = json.dumps(package)
        await self.websocket.send(package)
    
    async def listen_for_messages(self):
        while True:
            message = await self.websocket.recv()
            message = self.load_message(message)

    def load_message(self, raw_message: str):
        try:
            message = json.loads(raw_message)
            return message
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        
    async def start_listening(self):
        self.create_task(self.listen_for_messages())
        
    
