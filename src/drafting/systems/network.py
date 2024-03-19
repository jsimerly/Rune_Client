from ecs_engine.system import System, subscribe_to_event
from src.network import NetworkManager, MessageType

class NetworkSystem(System):
    nextwork = NetworkManager()

    @subscribe_to_event('update_dt')
    def update(self, dt):
        self.nextwork.run_one()
        messages = self.nextwork.read_queue()
        for message in messages:
            self.route_message(message)
            message = self.nextwork.decode_json(message)
 
    def route_message(self, message: MessageType):
        message = self.nextwork.decode_json(message)
        if message['type'] == 'draft':
            if message['data']['type'] == 'draft_update':
                self.publish_event('recv_draft_update', message=message)

            if message['data']['type'] == 'force_selection':
                self.publish_event('recv_force_selection', message=message)
    