from __future__ import annotations
from src.ui.components.visual import *
from src.ui.components.interactable import ClickableRectComponent
from src.ui.components.animation import UIAnimationComponent
from src.ui.font_singleton import FontManager
from src.utility.sizing import calculate_component_pos_rect, calculate_component_text_pos
from ecs_engine import Builder
import pygame

from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from ecs_engine import Entity

font_manager = FontManager()

class UIBuilder(Builder):

    def build_double_border_animation(self) -> Entity:
        return self.create_component(
             UIAnimationComponent,
                animation_id='double_border',
                start_time = pygame.time.get_ticks(),
                duration_ms = 300,
                state='start'
        )

    def build_decor(self,
            size: tuple[int, int], pos: tuple[int, int],
            rect_attributes: dict[str, Any] | None = None, rect_focus_attributes: dict[str, Any] = None,
            text:str = None, text_attributes: dict[str, Any] | None = None, text_focus_attributes: dict[str, Any] = None,
            image: pygame.Surface | None = None, image_alignment: str = 'center', image_margin: int = 0,
            markers: list[Type[Component]] = []
        ) -> Entity:
         
        return self.build_entity(
              self._build_rect_decoration_components(
                    size=size, pos=pos,
                    rect_attributes=rect_attributes, rect_focus_attributes=rect_focus_attributes,
                    text=text, text_attributes=text_attributes, text_focus_attributes=text_focus_attributes,
                    image=image, image_alignment=image_alignment, image_margin=image_margin,
                    markers=markers
              )
        )
    
    def build_button(self,
            size: tuple[int, int], pos: tuple[int, int], trigger_event:str, trigger_event_kwargs: dict = {},
            rect_attributes: dict[str, Any] | None = None, rect_focus_attributes: dict[str, Any] = None,
            text:str = None, text_attributes: dict[str, Any] | None = None, text_focus_attributes: dict[str, Any] = None,
            image: pygame.Surface | None = None, image_alignment: str = 'center', image_margin: int = 0,
            markers: list[Component] = []
        ) -> Entity:
        
        return self.build_entity(
              self._build_rect_button_components(
                    size=size, pos=pos, trigger_event=trigger_event, trigger_event_kwargs=trigger_event_kwargs,
                    rect_attributes=rect_attributes, rect_focus_attributes=rect_focus_attributes,
                    text=text, text_attributes=text_attributes, text_focus_attributes=text_focus_attributes,
                    image=image, image_alignment=image_alignment, image_margin=image_margin,
                    markers=markers
              )
         )

    def _build_rect_decoration_components(self,
            size: tuple[int, int], pos: tuple[int, int],
            rect_attributes: dict[str, Any] | None, rect_focus_attributes: dict[str, Any] | None,
            text:str, text_attributes: dict[str, Any] | None, text_focus_attributes: dict[str, Any],
            image: pygame.Surface | None = None, image_alignment: str = 'center', image_margin: int = 0,
            markers: list[Type[Component]] = []
        ) -> list[Component]:

            pos_component = self.create_component(
                UIComponent,
                    pos=pos
            )
            
            components = [pos_component]

            if rect_attributes:
                visual_componnet = self.create_component(
                    RectangleVisualComponent, 
                        size=size,
                        attributes=rect_attributes or {},
                        focus_attributes=rect_focus_attributes or {},
                )
                components.append(visual_componnet)

            if text:
                text_comp = self._build_text_component(text, text_attributes, text_focus_attributes, size, pos)
                components.append(text_comp)
            
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
                
            for marker in markers:
                components.append(marker)
    
            return components
    
    def _build_text_component(self, text: str, text_attributes: dict[str, Any], text_focus_attributes: dict[str, Any], size: tuple[int, int], pos: tuple[int, int]):

        if text_attributes:
            text_size = text_attributes.get('size', 36)
            font = text_attributes.setdefault('font', pygame.font.SysFont(None, text_size))
            text_alignment = text_attributes.get('alignment', 'center')
            text_margin = text_attributes.get('margin', 0)
        else:
            font: pygame.font.Font = pygame.font.SysFont(None, 36)
            text_alignment = 'center'
            text_margin = 0

        text_rect = font.size(text)
        text_pos = calculate_component_pos_rect(
            text_alignment, 
            size, 
            pos, 
            text_rect, 
            text_margin
        )

        return self.create_component(
            TextVisualComponent,
                text=text, 
                pos=text_pos,
                attributes=text_attributes or {},
                focus_attributes=text_focus_attributes or {}
            )
            
    def _build_rect_button_components(self,
            size: tuple[int, int], pos: tuple[int, int], trigger_event: str, trigger_event_kwargs: dict,
            rect_attributes: dict[str, Any] | None, rect_focus_attributes: dict[str, Any] | None,
            text:str, text_attributes: dict[str, Any] | None, text_focus_attributes: dict[str, Any],
            image: pygame.Surface | None = None, image_alignment: str = 'center', image_margin: int = 0,
            markers: list[Type[Component]] = []
        ) -> list[Component]:
            
            components = self._build_rect_decoration_components(
                size=size, pos=pos, 
                rect_attributes=rect_attributes, rect_focus_attributes=rect_focus_attributes,
                text=text, text_attributes=text_attributes, text_focus_attributes=text_focus_attributes,
                image=image, image_alignment=image_alignment, image_margin=image_margin,
                markers=markers
            )

            rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
            components.append(
                 self.create_component(
                    ClickableRectComponent,
                        rect=rect, 
                        event_name=trigger_event,  
                        event_kwargs=trigger_event_kwargs
                 )
            )
    
            return components

    @staticmethod
    def _calculate_component_pos_rect(alignment: str, container_size: tuple[int, int], container_pos: tuple[int, int], component_size: tuple[int, int], margin: int) -> tuple[int, int]:
        return calculate_component_pos_rect(alignment, container_size, container_pos, component_size, margin)
        