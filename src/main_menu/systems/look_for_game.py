from ecs_engine.system import System, subscribe_to_event
from src.main_menu.components.match_making_singleton import MatchMakingSingletonComponent
from src.global_singleton_comps import ScreenSingletonComponent
from src.main_menu.components.markers import MainMenuButtonMarker
from src.user.user import User
from src.ui.builders import UIBuilder
from src.ui.components.animation import UIAnimationComponent
from src.network import NetworkManager, MessageType
from datetime import datetime
import pygame

class LookForGame(System):
    network = NetworkManager()

    @subscribe_to_event('recv_login')
    def handle_login(self, message: MessageType):
        if message['data']['status'] == 'Success':
            screen_size = self.get_singleton_component(ScreenSingletonComponent).screen.get_size()
            ui_builder = self.get_builder(UIBuilder)

            button_size = (
                int(screen_size[0]*.3),
                int(screen_size[1]*.075),
            )
            button_pos = (
                int(screen_size[0]*.35),
                int(screen_size[1]*.75)
                )
            
            button_info = [
                {
                    'text': 'Start Game', 'trigger_event': 'start_game_clicked', 'markers': [MainMenuButtonMarker('start_game')],
                    'text_attributes': { 'color' : (0, 0, 0),'size' : 28},
                    'rect_attributes' : {'bg_color': (100, 100, 100), 'radius': 5},
                },
                {
                    'text': 'Settings', 'trigger_event': 'settings_clicked', 'markers': [MainMenuButtonMarker('settings')],
                    'text_attributes': { 'color' : (0, 0, 0),'size' : 28},
                    'rect_attributes' : {'bg_color': (100, 100, 100), 'radius': 5},
                },
                {
                    'text': 'Exit', 'trigger_event': 'exit_clicked', 'markers': [MainMenuButtonMarker('exit')],
                    'text_attributes': { 'color' : (0, 0, 0),'size' : 28},
                    'rect_attributes' : {'bg_color': (100, 100, 100), 'radius': 5},
                },
            ]
            
            for button_kwargs in button_info:
                button = ui_builder.build_button(
                    size=button_size,
                    pos=button_pos,
                    **button_kwargs
                )
                button_pos = (button_pos[0], button_pos[1] + button_size[1] + 3)

    @subscribe_to_event('start_game_clicked')
    def handle_start_game_clicked(self):
        match_making_comp = self.get_singleton_component(MatchMakingSingletonComponent)
        start_looking = not match_making_comp.looking_for_game

        message = {'start_looking': start_looking}
        self.network.send_message(User().serialized, type='match_making', serialized_message=message)

        main_menu_entities = self.get_entities_intersect([MainMenuButtonMarker])
        for button in main_menu_entities:
            mm_marker = button.get_component(MainMenuButtonMarker)
            if mm_marker.type == 'start_game':
                self.attach_component_to_entity(
                    button, 
                    UIAnimationComponent('blinking_in_queue', None)
                )

    @subscribe_to_event('exit_clicked')
    def handle_exit_clicked(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    @subscribe_to_event('recv_match_making')
    def handle_message_match_making(self, message: MessageType):
        if message['data']['status'] == 'looking_for_game':
            match_making_comp = self.get_singleton_component(MatchMakingSingletonComponent)
            match_making_comp.looking_for_game = True
            match_making_comp.start_queue_time = datetime.now()
            return

        if message['data']['status'] == 'cancel_looking_for_game':
            match_making_comp = self.get_singleton_component(MatchMakingSingletonComponent)
            match_making_comp.looking_for_game = False
            match_making_comp.start_queue_time = None
            return
            
        if message['data']['status'] == 'match_found':
            self.publish_event('match_found', message=message['data'])

        
   






        