from __future__ import annotations
import pygame
from ui.components.visual import *
from ui.components.interactable import ClickableRectComponent
from ui.font_singleton import FontManager
from utility.sizing import calculate_component_pos_rect, calculate_component_text_pos
from ecs_engine import Builder

from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from ecs_engine import Entity

font_manager = FontManager()

class UIBuilder(Builder):

    def build_decor(self,
            size: tuple[int, int], pos: tuple[int, int],
            bg_color: tuple[int, int, int] | None = (255,255,255), 
            border: int | None = None, border_color: int = (0, 0, 0), border_radius: int = 0, font_path: str = None,
            text: str | None = None, text_color: tuple[int, int, int] = (0,0,0), text_size: int = 24, text_alignment: str = 'center', text_margin: int = 0,
            image: pygame.Surface | None = None, image_alignment: str = 'center', image_margin: int = 0,
            markers: list[Type[Component]] = []
        ) -> Entity:
         
        return self.build_entity(
              self._build_rect_decoration_components(
                    size=size, pos=pos, bg_color=bg_color, 
                    border=border, border_color=border_color, border_radius=border_radius, font_path=font_path,
                    text=text, text_color=text_color, text_size=text_size, text_alignment=text_alignment, text_margin=text_margin,
                    image=image, image_alignment=image_alignment, image_margin=image_margin,
                    markers=markers
              )
         )
    
    def build_button(self,
            size: tuple[int, int], pos: tuple[int, int], trigger_event: str,
            bg_color: tuple[int, int, int] | None = (255,255,255), 
            border: int | None = None, border_color: int = (0, 0, 0), border_radius: int = 0, font_path: str = None,
            text: str | None = None, text_color: tuple[int, int, int] = (0,0,0), text_size: int = 24, text_alignment: str = 'center', text_margin: int = 0,
            image: pygame.Surface | None = None, image_alignment: str = 'center', image_margin: int = 0,
            markers: list[Type[Component]] = []
        ) -> Entity:
        
        return self.build_entity(
              self._build_rect_button_components(
                    size=size, pos=pos, bg_color=bg_color, trigger_event=trigger_event,
                    border=border, border_color=border_color, border_radius=border_radius, font_path=font_path,
                    text=text, text_color=text_color, text_size=text_size, text_alignment=text_alignment, text_margin=text_margin,
                    image=image, image_alignment=image_alignment, image_margin=image_margin,
                    markers=markers
              )
         )
    

    def _build_rect_decoration_components(self,
            size: tuple[int, int], pos: tuple[int, int],
            bg_color: tuple[int, int, int] | None = (255,255,255), 
            border: int | None = None, border_color: int = (0, 0, 0), border_radius: int = 0, font_path: str = None,
            text: str | None = None, text_color: tuple[int, int, int] = (0,0,0), text_size: int = 24, text_alignment: str = 'center', text_margin: int = 0,
            image: pygame.Surface | None = None, image_alignment: str = 'center', image_margin: int = 0,
            markers: list[Type[Component]] = []
        ) -> list[Component]:
            
            visual_componnet = self.create_component(
                RectangleVisualComponent, 
                    size=size,
                    bg_color=bg_color,
                    border=border,
                    border_color=border_color,
                    border_radius=border_radius,
            )
            pos_component = self.create_component(
                UIPositionComponent,
                    pos=pos
            )
            
            components = [visual_componnet, pos_component]

            if text:
                font = font_manager.get_font(font_path, text_size)
                text_rect = font.size(text)
                text_pos = calculate_component_pos_rect(
                    text_alignment, 
                    size, 
                    pos, 
                    text_rect, 
                    text_margin
                )
                components.append(
                     self.create_component(
                        TextVisualComponent,
                            text=text, 
                            text_color=text_color, 
                            font=font,
                            size=text_size,
                            pos=text_pos, 
                            margin=text_margin,
                            alignment=text_alignment,
                    )
                )
            
            if image:
                image_size = image.get_size()
                image_pos = self._calculate_component_pos_rect(image_alignment, size, pos, image_size, image_margin)
                components.append(
                    self.create_component(
                        ImageComponent,
                            image=image, 
                            pos=image_pos
                        )
                    )
                
            for Marker in markers:
                components.append(Marker())
    
            return components

    def _build_rect_button_components(self,
            size: tuple[int, int], pos: tuple[int, int], trigger_event: str,
            bg_color: tuple[int, int, int] | None = (255, 255, 255),
            border: int | None = None, border_color: int = (0, 0, 0), border_radius: int = 0,
            text: str | None = None, text_color: tuple[int,int,int]=(0,0,0), text_size: int = 12, text_alignment: str = 'center', text_margin: int = 0, font_path: str = None,
            image: pygame.Surface | None = None, image_alignment: str = 'center', image_margin: int = 0,
            markers: list[Type[Component]] = []
        ) -> list[Component]:
            
            components = self._build_rect_decoration_components(
                size=size, pos=pos, bg_color=bg_color, border=border, border_color=border_color, border_radius=border_radius, text=text, text_size=text_size, text_color=text_color, text_alignment=text_alignment, text_margin=text_margin, font_path=font_path, image=image, image_alignment=image_alignment, image_margin=image_margin,
                markers=markers
            )

            rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
            components.append(
                 self.create_component(
                    ClickableRectComponent,
                        rect=rect, 
                        event_name=trigger_event  
                 )
            )
    
            return components

    @staticmethod
    def _calculate_component_pos_rect(alignment: str, container_size: tuple[int, int], container_pos: tuple[int, int], component_size: tuple[int, int], margin: int) -> tuple[int, int]:
        return calculate_component_pos_rect(alignment, container_size, container_pos, component_size, margin)
        