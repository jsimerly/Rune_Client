from ecs_engine import Component
from dataclasses import dataclass, field
import pygame

@dataclass
class UIPositionComponent(Component):
    pos: tuple[int, int]

@dataclass
class RectangleVisualComponent(Component):
    size: tuple[int, int]
    bg_color: tuple[int, int, int] | None
    border: int = 0
    border_color: tuple[int, int, int] = (0, 0, 0)
    border_radius: int = 0

@dataclass
class TextVisualComponent(Component):
    text: str
    text_color: tuple[int, int, int]
    font: pygame.font.Font
    alignment: str
    margin: int
    size: int
    pos: tuple[int, int]

    @property
    def text_size(self) -> tuple[int, int]:
        return self.font.size(self.text)
    
@dataclass
class ImageComponent(Component):
    image: pygame.Surface
    pos: tuple[int, int]

