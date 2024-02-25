from ecs_engine import Component
from dataclasses import dataclass
import pygame

# to make non rect we'll have to update this to clickableComponent and use a pygame.mesh
@dataclass
class ClickableRectComponent(Component):
    rect: pygame.Rect
    event_name: str
