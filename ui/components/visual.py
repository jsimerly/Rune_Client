from ecs_engine import Component
from dataclasses import dataclass, field
from typing import Any, TypedDict
import pygame

@dataclass 
class Border:
    thickness: int = 1
    color: tuple[int, int, int] = (0, 0, 0)

@dataclass
class UIComponent(Component):
    pos: tuple[int, int]
    in_focus: bool = field(default=False)

class RectAttrDict(TypedDict):
    bg_color: tuple[int, int, int]
    radius: int
    border_thickness: int
    border_color: tuple[int, int, int] 
    border_radius: int
@dataclass
class RectangleVisualComponent(Component):
    size: tuple[int, int]
    attributes: RectAttrDict
    focus_attributes: RectAttrDict

    def __post_init__(self):
        default_attr = {
            'bg_color': (255, 255, 255),
            'radius': 0,
            'border_thickness': 1,
            'border_color': (0, 0, 0),
        }
        default_focus_attr = {
            'bg_color': (255, 255, 255),
            'radius': 0,
            'border_thickness': 1,
            'border_color': (0, 0, 0),
        }

        self.attributes = {**default_attr, **self.attributes}
        self.focus_attributes = {**default_focus_attr, **self.focus_attributes}

class TextAttrDict(TypedDict):
    font: pygame.font.Font
    color: tuple[int, int, int]
    alignment: str
    margin: int
    size: int
@dataclass
class TextVisualComponent(Component):
    text: str
    pos: tuple[int, int]
    attributes : TextAttrDict
    focus_attributes: TextAttrDict

    def __post_init__(self):
        default_attr = {
            'font': pygame.font.Font(None, 36),
            'color': tuple[int, int, int],
            'alignment': 'center',
            'margin': 0,
        }

        default_focus_attr = {
            'font': pygame.font.Font(None, 36),
            'color': tuple[int, int, int],
            'alignment': 'center',
            'margin': 0,
        }

        self.attributes = {**default_attr, **self.attributes}
        self.focus_attributes = {**default_focus_attr, **self.attributes, **self.focus_attributes}

    @property
    def text_size(self) -> tuple[int, int]:
        return self.attributes['font'].size(self.text)
    
    
@dataclass
class ImageComponent(Component):
    image: pygame.Surface
    pos: tuple[int, int]

