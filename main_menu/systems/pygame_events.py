from __future__ import annotations
from ecs_engine.system import System, subscribe_to_event
from ui.components.interactable import ClickableRectComponent
from main_menu.components.input_singleton import MenuInputSingletonComponent
from ui.components.visual import TextVisualComponent, RectangleVisualComponent, UIComponent
from main_menu.components.markers import LoginButtonMarker, LoginInputMarker
from utility.sizing import calculate_component_pos_rect
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_engine import Entity

class PygameEventsSystem(System):
    required_components = [ClickableRectComponent]

    @subscribe_to_event('update_dt')
    def update(self, dt: int):  
        input_comp = self.get_singleton_component(MenuInputSingletonComponent)
        entities = self.get_required_entities()

        for event in input_comp.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown(event, input_comp, entities)

            if event.type == pygame.KEYDOWN:
                self._handle_keydowns(event.unicode, input_comp)

    def _handle_mousedown(self, event: pygame.event.Event, input_comp: MenuInputSingletonComponent, entities: list[Entity]):
        unfocus = True
        for entity in entities:
            clickable_comp = entity.get_component(ClickableRectComponent)
            ui_comp = entity.get_component(UIComponent)
            if clickable_comp.rect.collidepoint(event.pos):
                ui_comp.in_focus = True
                input_comp.current_focus = entity.id
                unfocus = False

                self.publish_event(clickable_comp.event_name)
            else:
                ui_comp.in_focus = False

        if unfocus:
            input_comp.current_focus = None

    def _handle_keydowns(self, key: str, input_comp: MenuInputSingletonComponent):
        if input_comp.current_focus is not None:
            current_focus = self.get_entity(input_comp.current_focus)
            if current_focus.has_component(LoginInputMarker):
                text_comp = current_focus.get_component(TextVisualComponent)
                if key == '\x08':
                    text_comp.text = text_comp.text[:-1]
                else:
                    text_comp.text += key







                
                        

                      



        
            