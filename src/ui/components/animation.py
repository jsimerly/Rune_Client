from ecs_engine import Component
from dataclasses import dataclass, field
from typing import Any, Literal
import pygame

# to make non rect we'll have to update this to clickableComponent and use a pygame.mesh
@dataclass
class UIAnimationComponent(Component):
    animation_id: str
    duration_ms: int | None
    start_time: int = pygame.time.get_ticks()
    state: Literal['start', 'active', 'end'] = field(default='start')