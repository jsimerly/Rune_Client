from __future__ import annotations
from ecs_engine import EcsAdmin, subscribe_to_event
import pygame
import os

from src.interfaces import AbstractClientState
from src.client_state import ClientState
from src.ui.builders import UIBuilder
from src.global_singleton_comps import ScreenSingletonComponent
from src.ui.systems.render_ui import RenderUISystem

from .systems.input import InputSystem
from .systems.pygame_events import PygameEventsSystem
from .systems.login_system import LogInSystem
from .systems.network import NetworkSystem, MessageType
from .components.input_singleton import MenuInputSingletonComponent
from .systems.look_for_game import LookForGame
from .systems.animation import MainMenuUIAnimationSystem
from .components.match_making_singleton import MatchMakingSingletonComponent
from .components.markers import *



from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ecs_engine import Entity

client_state = ClientState()

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

class MainMenu(EcsAdmin, AbstractClientState):
    events = [
        'update_dt', 'pygame_events', 'login_clicked', 'login_input_clicked', 'look_for_game_click', 'cancel_lfg', 'recv_login', 'start_game_clicked', 'settings_clicked', 'exit_clicked', 'recv_match_making', 'match_found'
    ]
    systems = [
       InputSystem, PygameEventsSystem, NetworkSystem, 
       LookForGame,  LogInSystem, 
       MainMenuUIAnimationSystem, RenderUISystem,
    ]
    singleton_components = [
        ScreenSingletonComponent(
            screen=pygame.display.set_mode(client_state.screen_size, pygame.SRCALPHA), 
            bg_color=(40, 40, 40)
        ),
        MenuInputSingletonComponent(),
        MatchMakingSingletonComponent()
    ]
    builders = [UIBuilder]

    def __init__(self, max_entities: int = 1000):
        super().__init__(max_entities)
        self.fps = client_state.fps
        self.clock = pygame.time.Clock()

    def on_enter(self, _):
        self._create_initial_entities()

    def update(self):
        dt: int = self.clock.tick(self.fps)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                client_state.close()

        self.publish_event('pygame_events', events=events)
        self.publish_event('update_dt', dt=dt)
    
        pygame.display.flip()

    @subscribe_to_event('match_found')
    def handle_transition_to_draft(self, message: MessageType):
        client_state.update_state('draft', message)

    def _create_initial_entities(self):
        self._create_buttons()
        self._create_decor()
       
    def _create_decor(self) -> list[Entity]:
        screen_size = self.get_singleton_component(ScreenSingletonComponent).screen.get_size()
            
        img_path = os.path.join(current_dir, 'assets', 'rune_logo.png')
        game_logo = pygame.image.load(img_path).convert_alpha()
        original_logo_size = game_logo.get_size()  
        new_height = int(screen_size[1] * 0.5)
        aspect_ratio = original_logo_size[0] / original_logo_size[1]
        new_width = int(new_height * aspect_ratio)
        logo_size = (new_width, new_height)
        
        logo_pos = (int((screen_size[0] - logo_size[0]) * 0.5), int(screen_size[1] * 0.05))
        
        game_logo = pygame.transform.scale(game_logo, logo_size)
        
        ui_builder = self.get_builder(UIBuilder)
        decor_entities = [
            ui_builder.build_decor(logo_size, logo_pos, image=game_logo, rect_attributes = {'bg_color': None, 'border_thickness': 0})
        ]
        return decor_entities

    def _create_buttons(self) -> list[Entity]:
        screen_size = self.get_singleton_component(ScreenSingletonComponent).screen.get_size()
        button_size = (
            int(screen_size[0]*.3),
            int(screen_size[1]*.075),
        )
        button_pos = (
            int(screen_size[0]*.35),
            int(screen_size[1]*.80)
        )

        button_info = [
            {
                'text': ' ', 'trigger_event': 'login_input_clicked', 'markers': [LoginMarker('username_input')],
                'text_attributes': {'alignment': 'center_left', 'margin': 10, 'color': (0,0,0), 'size': 28},
                'rect_attributes' : {'bg_color': (240, 240, 240), 'radius': 5},
                'rect_focus_attributes': {'border_color':(204, 161, 237), 'border_thickness': 2, 'radius': 5}

            },
            {
                'text': 'Login', 'trigger_event': 'login_clicked', 'markers': [LoginMarker('button')],
                'text_attributes': { 'color' : (0, 0, 0),'size' : 28},
                'rect_attributes' : {'bg_color': (100, 100, 100), 'radius': 5},
            },
        ]
        
        buttons: list[Entity] = []
        ui_builder = self.get_builder(UIBuilder)
        
        for button_kwargs in button_info:
            button = ui_builder.build_button(
                size=button_size,
                pos=button_pos,
                **button_kwargs
            )
            button_pos = (button_pos[0], button_pos[1] + button_size[1] + 3)
            buttons.append(button)

        return buttons
