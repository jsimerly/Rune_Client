from __future__ import annotations
import asyncio
import websockets
from typing import Callable
import json
from typing import TYPE_CHECKING, Any, TypedDict

if TYPE_CHECKING:
    from user.user import User

class MessageType(TypedDict):
    type: str
    data: dict

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
        self.connect_event = asyncio.Event()
        self.message_queue = []

    def connect(self):
        asyncio.run_coroutine_threadsafe(self._connect(), self.loop)
        self.loop.run_until_complete(self.connect_event.wait())

    async def _connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connect_event.set()
        except Exception as e:
            print(f"Failed to connect: {e}")
            return
        await self.start_listening()
       
    def close_connection(self):
        if not self.loop.is_running():
            self.loop.run_until_complete(self._close_connection())

    async def _close_connection(self):
        try:
            if self.websocket:
                await self.websocket.close()
                print('Websocket connection was closed normally.')
        except Exception as e:
            print(f"Exception in _close_connection: {e}")

    def create_task(self, task: Callable):
        self.loop.create_task(task)

    def run_one(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    def decode_json(self, message: dict) -> MessageType:
        try: 
            message_json = json.loads(message)
        except json.JSONDecodeError:
            print('Recieved an invalid JSON string,')
            return 
        return message_json

    def send_message(self, user: User, type: str, serialized_message: str):
        self.create_task(self._send_message(user, type, serialized_message))

    async def _send_message(self, user: User, type: str, message: dict):
        if not isinstance(message, dict):
            raise ValueError('Messages must in a dictionry or json format to be sent using send_data.')
 
        if not self.websocket:
            await self._connect()

        package = {
            'type': type,
            'user': user, #.serializer()
            'data': message,
        }
        package = json.dumps(package)
        await self.websocket.send(package)
    
    async def listen_for_messages(self):
        try:
            while True:
                message = await self.websocket.recv()
                self.message_queue.append(message)
        except websockets.exceptions.ConnectionClosedOK:
            ...

    def read_queue(self) -> list[Any]:
        messages = self.message_queue.copy()  
        self.message_queue.clear() 
        return messages
        
    def start_listening(self):
        self.create_task(self.listen_for_messages())
        
    
