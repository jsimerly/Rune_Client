from ecs_engine import SingletonComponent
from typing import TypedDict, Literal
from dataclasses import dataclass, field


class TeamType(TypedDict):
    id: str
    user: dict
    bans: list[dict]
    picks: list[dict]

class CharacterType(TypedDict):
    display_name: str
    char_id: int
    banned: bool = False
    picked: bool = False

    role: Literal['tank', 'damage', 'support']

    damage: int
    durability: int
    utility: int
    difficulty: int

@dataclass
class DraftStateSingletonComponent(SingletonComponent):
    id: str
    active: bool 
    current_phase: int

    last_action_time_ms: int 
    map: str

    client_team: Literal['team_1', 'team_2'] 
    team_1: TeamType
    team_2: TeamType

    characters: dict[int, CharacterType] 
    available_picks: list[int]
    unavailable_picks: list[int] 

    state: Literal['pre_draft', 'team_1_ban', 'team_2_ban', 'team_1_pick', 'team_2_pick', 'completed'] = field(default='pre_draft')


