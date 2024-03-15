from ecs_engine import Component, SingletonComponent
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

@dataclass
class SelectedCharacterSingleton(SingletonComponent):
    char_id: int = None
