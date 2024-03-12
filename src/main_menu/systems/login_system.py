from ecs_engine.system import System, subscribe_to_event
from src.main_menu.components.match_making_singleton import MatchMakingSingletonComponent
from src.ui.components.visual import TextVisualComponent, RectangleVisualComponent
from src.main_menu.components.markers import LoginMarker
from src.user.user import User
from src.network import NetworkManager, MessageType
from datetime import datetime

class LogInSystem(System):
    required_components = [LoginMarker]
    network = NetworkManager()

    @subscribe_to_event('login_clicked')
    def login_clicked(self):
        inputs = self.get_required_entities()
        for input in inputs:
            input_type = input.get_component(LoginMarker).type
            if input_type == 'username_input' or input_type == 'password_input':
                value = input.get_component(TextVisualComponent).text.strip(' ')

                if value == '' or value is None:
                    rect_comp = input.get_component(RectangleVisualComponent)
                    rect_comp.attributes['border_color'] = (255, 0, 0)
                    return
    
                username = value
                
        self.network.send_message(user=None, type='login', serialized_message={'username': username})

    @subscribe_to_event('recv_login')
    def handle_login(self, message: MessageType):
        if message['data']['status'] == 'Success':
            login_entities = self.get_entities_union([LoginMarker])
            user = User(user=message['data']['user'])
            for entity in login_entities:
                self.destroy_entity(entity)
                
        

  



        