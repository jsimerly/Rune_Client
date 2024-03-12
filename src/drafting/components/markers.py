from ecs_engine import Component
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class DraftBoxMarker(Component):
    team: Literal['team_1', 'team_2']
    state: Literal['idle', 'active', 'complete'] = field(default='idle')
    order: int

@dataclass
class CharacterButtonMarker(Component):
    id: int
