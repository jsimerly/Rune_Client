from ecs_engine import SingletonComponent
from dataclasses import dataclass, field
import pygame

@dataclass
class DraftInputSingletonComponent(SingletonComponent):
    events: list[pygame.event.Event] = field(default_factory=list)
    current_focus: int = field(default=None)
