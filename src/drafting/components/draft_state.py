from ecs_engine import SingletonComponent
from typing import TypedDict, Literal
from dataclasses import dataclass, field

class UserType(TypedDict):
    username: str

class TeamType(TypedDict):
    id: str
    user: UserType
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

    last_action_time_ms: int 
    map: str

    is_team_1: bool 
    team_1: TeamType
    team_2: TeamType

    available_picks: list[int]
    unavailable_picks: list[int] 

    state: Literal['pre_draft', 'team_1_ban', 'team_2_ban', 'team_1_pick', 'team_2_pick', 'completed'] = field(default='pre_draft')
    count_down_ms: int = field(default=10000) 

    @property
    def client_team(self) -> TeamType:
        if self.is_team_1:
            return self.team_1
        return self.team_2
    
    @property
    def oppo_team(self) -> TeamType:
        if self.is_team_1:
            return self.team_2
        return self.team_1
    
    @property
    def is_client_turn(self) -> bool:
        if self.is_team_1:
            return self.state == 'team_1_ban' or self.state == 'team_1_pick'
        return self.state == 'team_2_ban' or self.state == 'team_2_pick'

        

