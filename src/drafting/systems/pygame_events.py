from ecs_engine import System, subscribe_to_event, Entity
from src.ui.components.interactable import ClickableRectComponent
from src.ui.components.visual import UIComponent
from src.drafting.components.input_singleton import DraftInputSingletonComponent
from src.drafting.components.character import DraftCharacterComponent, SelectedCharacterSingleton
import pygame

class PygameEventsSystem(System):
    required_components = [ClickableRectComponent]

    @subscribe_to_event('update_dt')
    def update(self, dt: int):
        input_comp = self.get_singleton_component(DraftInputSingletonComponent)
        entities = self.get_required_entities()
 
        for event in input_comp.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event, input_comp, entities)

    def _handle_mouse_down(self, event: pygame.event.Event, input_comp: DraftInputSingletonComponent, entities: list[Entity]):
        unfocus = True
        for entity in entities:
            clickable_comp = entity.get_component(ClickableRectComponent)
            ui_comp = entity.get_component(UIComponent)

            if clickable_comp.rect.collidepoint(event.pos):
                ui_comp.in_focus = True
                input_comp.current_focus = entity.id
                unfocus = False
                self._check_for_icon(entity)
            else:
                ui_comp.in_focus = False

        if unfocus:
            input_comp.current_focus = None

    def _check_for_icon(self, entity: Entity):
        char_comp = entity.get_component(DraftCharacterComponent)
        if char_comp:
            selected_char = self.get_singleton_component(SelectedCharacterSingleton)
            selected_char.char_id = char_comp.char_id

    