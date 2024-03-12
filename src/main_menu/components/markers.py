from ecs_engine import Component
from dataclasses import dataclass

@dataclass
class MainMenuButtonMarker(Component):
    type: str

@dataclass
class LoginMarker(Component):
    type: str
