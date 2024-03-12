
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

    def route_message(self, message: MessageType):
        message = self.nextwork.decode_json(message)
        if message['type'] == 'login':
            self.publish_event('recv_login', message=message)
        
        if message['type'] == 'match_making':
            self.publish_event('recv_match_making', message=message)


    

    



        