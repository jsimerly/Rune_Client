from __future__ import annotations
from src.interfaces import AbstractClientState
from src.client_state import ClientState
from src.global_singleton_comps import ScreenSingletonComponent
from src.drafting.components.input_singleton import DraftInputSingletonComponent
from src.drafting.components.draft_state import DraftStateSingletonComponent
from ecs_engine import EcsAdmin
from src.ui.systems.render_ui import RenderUISystem
from src.ui.builders import UIBuilder
from src.drafting.systems.input import InputSystem
from typing import TypedDict, Literal
import pygame

client_state = ClientState()
class NetworkTeamJson(TypedDict):
    id: str
    user: dict
    bans: list[dict]
    picks: list[dict]

class CharacterDict(TypedDict):
    display_name: str
    char_id: int
    banned: bool = False
    picked: bool = False

    role: Literal['tank', 'damage', 'support']

    damage: int
    durability: int
    utility: int
    difficulty: int

class NetworkDraftInfo(TypedDict):
    id: str
    team_1: NetworkTeamJson
    team_2: NetworkTeamJson
    current_phase: int
    characters: dict[int, CharacterDict]
    available: list[int]
    unavailable: list[int]

class NetworkDraftPackage(TypedDict):
    status: str
    map: str
    draft: NetworkDraftInfo
    is_team_1: bool

class Drafting(EcsAdmin, AbstractClientState):
    events = ['update_dt', 'pygame_events']
    builders = [UIBuilder]
    systems = [
        InputSystem,
        RenderUISystem
    ]
    singleton_components = [
        ScreenSingletonComponent(
            screen=pygame.display.set_mode(client_state.screen_size, pygame.SRCALPHA), 
            bg_color=(40, 40, 40)
        ),
        DraftInputSingletonComponent(),
    ]
    
    def __init__(self, max_entities: int = 1000):
        super().__init__(max_entities)
        self.fps = client_state.fps
        self.clock = pygame.time.Clock()
        self.draft = None

        self._create_ui()

    def on_enter(self, load_data: NetworkDraftPackage):
        draft_state_singleton = DraftStateSingletonComponent(
            id = load_data['draft']['id'],
            active = True,
            current_phase = load_data['draft']['current_phase'],
            last_action_time_ms = pygame.time.get_ticks(),
            map = load_data['map'],
            client_team = load_data['is_team_1'],
            team_1 = load_data['draft']['team_1'],
            team_2 = load_data['draft']['team_2'],

            characters = load_data['draft']['character_info'],
            available_picks = load_data['draft']['available'],
            unavailable_picks = load_data['draft']['unavailable'],
        )
        self.add_singleton_component(draft_state_singleton)

    def update(self):
        dt: int = self.clock.tick(self.fps)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                client_state.close()
    
        self.publish_event('pygame_events', events=events)
        self.publish_event('update_dt', dt=dt)
        pygame.display.flip()

    def _create_ui(self):
        screen_comp = self.get_singleton_component(ScreenSingletonComponent)
        self._create_draft_boxes(screen_comp)
        self._create_character_icons(screen_comp)
        self._create_character_info_dashboards(screen_comp)

    def _create_draft_boxes(self, screen_comp: ScreenSingletonComponent):
        screen_size = screen_comp.screen.get_size()
        box_ratio = .075
        box_size = (
            int(screen_size[0] * box_ratio), 
            int(screen_size[0] * box_ratio),
        )

        y_pos = screen_size[1] * .15
        x_offset = .04
        t1_x_pos = screen_size[0] * x_offset
        t2_x_pos = screen_size[0] * (1 - (x_offset + box_ratio)) 

        t1_pos = (t1_x_pos, y_pos)
        t2_pos = (t2_x_pos, y_pos)

        box_info = [
            {
                'rect_attributes': {
                    'radius': 5, 
                    'border_color': (255, 0,0), 
                    'border_thickness': 2,
                    'bg_color': None
                }
            },
            {
                'rect_attributes': {
                    'radius': 5, 
                    'border_color': (255, 255, 255),  
                    'border_thickness': 2,
                    'bg_color': None
                }
            },
            {
                'rect_attributes': {
                    'radius': 5, 
                    'border_color': (255, 255, 255),  
                    'border_thickness': 2,
                    'bg_color': None
                }
            },
            {
                'rect_attributes': {
                    'radius': 5, 
                    'border_color': (255, 255, 255),  
                    'border_thickness': 2,
                    'bg_color': None
                }
            },
        ]

        ui_builder = self.get_builder(UIBuilder)

        for box_kwargs in box_info:
            t1_box = ui_builder.build_decor(
                size=box_size,
                pos=t1_pos,
                **box_kwargs
            )
            t1_pos = (t1_pos[0], t1_pos[1] + box_size[1] + 5)
            t2_box = ui_builder.build_decor(
                size=box_size,
                pos=t2_pos,
                **box_kwargs
            )
            t2_pos = (t2_pos[0], t2_pos[1] + box_size[1] + 5)

    def _create_character_icons(self, screen_comp: ScreenSingletonComponent):
        ...

    def _create_character_info_dashboards(self, screen_comp: ScreenSingletonComponent):
        ...
