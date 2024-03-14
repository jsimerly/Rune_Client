from __future__ import annotations
from src.interfaces import AbstractClientState
from src.client_state import ClientState
from src.global_singleton_comps import ScreenSingletonComponent
from src.drafting.components.input_singleton import DraftInputSingletonComponent
from src.drafting.components.draft_state import DraftStateSingletonComponent, CharacterType
from src.drafting.components.character import DraftCharacterComponent
from src.drafting.components.markers import CountdownMarker, DraftBoxMarker
from ecs_engine import EcsAdmin
from src.ui.systems.render_ui import RenderUISystem
from src.ui.builders import UIBuilder
from src.drafting.systems.input import InputSystem
from typing import TypedDict, Literal
from src.drafting.systems.draft import DraftSystem
from src.drafting.characters import character_icons
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
    character_info: dict[int, CharacterDict]
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
        RenderUISystem,
        DraftSystem
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
            is_team_1 = load_data['is_team_1'],
            team_1 = load_data['draft']['team_1'],
            team_2 = load_data['draft']['team_2'],

            characters = load_data['draft']['character_info'],
            available_picks = load_data['draft']['available'],
            unavailable_picks = load_data['draft']['unavailable'],
        )
        self.add_singleton_component(draft_state_singleton)
        self._create_character_icons(load_data['draft']['character_info'])
        self._create_draft_info_decor(draft_state_singleton)

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
        self._create_character_info_dashboards(screen_comp)

    def _create_draft_boxes(self, screen_comp: ScreenSingletonComponent):
        screen_size = screen_comp.screen.get_size()
        box_ratio = .075
        box_size = (
            int(screen_size[0] * box_ratio), 
            int(screen_size[0] * box_ratio),
        )

        y_pos = screen_size[1] * .1
        x_offset = .04
        t1_x_pos = screen_size[0] * x_offset
        t2_x_pos = screen_size[0] * (1 - (x_offset + box_ratio)) 

        t1_pos = (t1_x_pos, y_pos)
        t2_pos = (t2_x_pos, y_pos)

        box_info = [
            {'rect_attributes': {'radius': 5, 'border_thickness': 1,'bg_color': None,
                'border_color': (255, 0, 0)}},
            {'rect_attributes': {'radius': 5, 'border_thickness': 1,'bg_color': None,
                'border_color': (255, 255, 255),  
            }},
            {'rect_attributes': {'radius': 5, 'border_thickness': 1,'bg_color': None,
                'border_color': (255, 255, 255),  
            }},
            {'rect_attributes': {'radius': 5, 'border_thickness': 1,'bg_color': None,
                'border_color': (255, 255, 255),  
            }},
        ]

        ui_builder = self.get_builder(UIBuilder)

        for box_kwargs in box_info:
            t1_box = ui_builder.build_decor(
                size=box_size,
                pos=t1_pos,
                markers=[DraftBoxMarker(order=1, team='team_1')],
                **box_kwargs
            )
            t1_pos = (t1_pos[0], t1_pos[1] + box_size[1] + 5)
            t2_box = ui_builder.build_decor(
                size=box_size,
                pos=t2_pos,
                markers=[DraftBoxMarker(order=1, team='team_2')],
                **box_kwargs
            )
            t2_pos = (t2_pos[0], t2_pos[1] + box_size[1] + 5)

    def _create_character_icons(self, characters: dict[int, CharacterType]):
        screen_comp = self.get_singleton_component(ScreenSingletonComponent)
     
        screen_size = screen_comp.screen.get_size()
        box_ratio = .075
        box_size = (
            int(screen_size[0] * box_ratio), 
            int(screen_size[0] * box_ratio),
        )

        base_box_attributes = {
            'rect_attributes': {
                'radius': 5, 
                'border_color': (80, 80, 80), 
                'border_thickness': 2,
                'bg_color': None
            },
        }

        ui_builder = self.get_builder(UIBuilder)

        x_offset = .175
        x_start_pos = screen_size[0] * x_offset
        x_pos = x_start_pos
        max_x_pos = screen_size[0] * (1 - x_offset)
        
        y_pos = screen_size[1] * .575

        icon_spacing = 10

        pos = (x_pos, y_pos)
        for char_id, char_info in characters.items():
            char_id = int(char_id)
            icon_image = pygame.transform.scale(character_icons[char_id], (box_size[0]-2, box_size[1]-2))
            char_comp = DraftCharacterComponent(
                char_id=char_id,
                display_name=char_info['display_name'],
                role=char_info['role'],
                damage=char_info['damage'],
                durability=char_info['durability'],
                utility=char_info['utility'],
                difficulty=char_info['difficulty'],
            )
        
            ui_builder.build_button(
                size=box_size,
                pos=pos,
                image=icon_image,
                markers=[char_comp],
                trigger_event='char_icon_selected',
                trigger_event_kwargs={'char_id': char_id},
                **base_box_attributes
            )

            x_pos = pos[0] + box_size[0] + icon_spacing
            if x_pos > max_x_pos:
                x_pos = x_start_pos
                y_pos += box_size[1] + icon_spacing

            pos = (x_pos, y_pos)

        self._create_lock_button(screen_comp, start_y= y_pos + box_size[1] + 20)

    def _create_lock_button(self, screen_comp: ScreenSingletonComponent, start_y: tuple[int,int]=None):
        screen_size = screen_comp.screen.get_size()
        ui_builder = self.get_builder(UIBuilder)

        if not start_y:
            start_y = screen_size[1] * .82
        size = (screen_size[0] * .16, screen_size[1] * .1)
        pos = (screen_size[0] * .5 - (size[0]/2), start_y)
        button_kwargs = {
            'text': 'Lock In',
            'text_attributes': {
                'alignment': 'center',
                'margin': 5,
                'color': (60, 60, 60),
                'size': 36
            },
            'rect_attributes': {
                'radius': 5, 
                'border_thickness': 0,
                'bg_color': (235, 204, 113)
            },
        }

        ui_builder.build_button(
            size=size,
            pos=pos,
            trigger_event='lock_in_clicked',
            **button_kwargs
        )

    def _create_draft_info_decor(self, draft_state: DraftStateSingletonComponent):
        screen_comp = self.get_singleton_component(ScreenSingletonComponent)
        screen_size = screen_comp.screen.get_size()

        team_base_kwargs = {
            'text_attributes': {
                'alignment': 'center',
                'margin': 5,
                'color': (160, 160, 160),
                'size': 46,
            },
            'text_focus_attributes': {
                'alignment': 'center',
                'margin': 5,
                'color': (255, 255, 255),
                'size': 46,
            }
        }
        
        team_text_offset = .0175
        team_text_box_size = (screen_size[0] * .125, screen_size[1] * .075)
        client_team_pos = (screen_size[0] * team_text_offset, screen_size[1] * .02)
        opp_team_pos = (screen_size[0] * (1-team_text_offset) - team_text_box_size[0], screen_size[1] * .02)

        ui_builder = self.get_builder(UIBuilder)
        client_team_info = ui_builder.build_decor(
            size=team_text_box_size,
            pos=client_team_pos,
            text=draft_state.client_team['user']['username'],
            **team_base_kwargs
        )
        opp_team_info = ui_builder.build_decor(
            size=team_text_box_size,
            pos=opp_team_pos,
            text=draft_state.oppo_team['user']['username'],
            **team_base_kwargs
        )

        header_kwargs = {
            'text_attributes': {
                'alignment': 'center',
                'margin': 5,
                'color': (160, 160, 160),
                'size': 28,
            },
        }
        header_size = (screen_size[0] * .4, screen_size[1] * .05)
        header_pos = (screen_size[0]* .5 - header_size[0]/2, 0)

        header = ui_builder.build_decor(
            size=header_size,
            pos=header_pos,
            text='Waiting for the draft to begin...',
            **header_kwargs
        )

        countdown_size = (screen_size[0] * .2, screen_size[1] * .1)
        countdown_pos = (screen_size[0]* .5 - countdown_size[0]/2, header_pos[1] + 10)
        countdown_kwargs = {
            'text_attributes': {
                'alignment': 'center',
                'margin': 5,
                'color': (160, 160, 160),
                'size': 40,
            },
        }
        count_down = ui_builder.build_decor(
            size=countdown_size,
            pos=countdown_pos,
            text='10s',
            markers=[CountdownMarker()],
            **countdown_kwargs,
        )

    def _create_character_info_dashboards(self, screen_comp: ScreenSingletonComponent):
        ...
