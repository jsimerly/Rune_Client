from __future__ import annotations
from ecs_engine.system import System, subscribe_to_event
from ui.components.interactable import ClickableRectComponent
from main_menu.components.input_singleton import MenuInputSingletonComponent
from ui.components.visual import TextVisualComponent, RectangleVisualComponent, UIPositionComponent
from utility.sizing import calculate_component_pos_rect
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_engine import Entity

class ButtonClickSystem(System):
    required_components = [ClickableRectComponent]

    @subscribe_to_event('update_dt')
    def update(self, dt: int):  
        input_comp = self.get_singleton_component(MenuInputSingletonComponent)

        for event in input_comp.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                entities = self.get_required_entities()

                for entity in entities:
                    clickable_comp = entity.get_component(ClickableRectComponent)
                    if clickable_comp.rect.collidepoint(event.pos):
                        self.publish_event(clickable_comp.event_name)
                        

                      



        
            