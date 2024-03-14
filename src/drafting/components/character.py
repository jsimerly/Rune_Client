from ecs_engine import Component
from dataclasses import dataclass
from typing import Literal
import pygame

@dataclass
class DraftCharacterComponent(Component):
    char_id: int
    display_name: int

    role: Literal['tank', 'damage', 'support']
    damage: int
    durability: int
    utility: int
    difficulty: int

    selected: bool = False
    banned: bool = False
    picked: bool = False
