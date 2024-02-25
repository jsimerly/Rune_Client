from ecs_engine import SingletonComponent
from dataclasses import dataclass
import pygame

@dataclass
class ScreenSingletonComponent(SingletonComponent):
    screen: pygame.Surface
    bg_color: tuple[int, int, int]