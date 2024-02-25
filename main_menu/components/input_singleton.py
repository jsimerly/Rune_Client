from ecs_engine import SingletonComponent
from dataclasses import dataclass, field
import pygame

@dataclass
class MenuInputSingletonComponent(SingletonComponent):
    events: list[pygame.event.Event] = field(default_factory=list)
