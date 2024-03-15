from ecs_engine.entity_admin import EcsAdmin
from ecs_engine.interfaces import IEventBus
from src.ui.systems.render_ui import RenderUISystem
from src.drafting.components.character import DraftCharacterComponent
from src.drafting.components.markers import CharacterButtonMarker
from src.ui.components.visual import RectangleVisualComponent, UIComponent
from src.global_singleton_comps import ScreenSingletonComponent
import pygame
from ecs_engine import subscribe_to_event

class DraftRenderUISystem(RenderUISystem):
    def __init__(self, ecs_admin: EcsAdmin, event_bus: IEventBus):
        super().__init__(ecs_admin, event_bus)

    @subscribe_to_event('update_dt')
    def update(self, dt: int):
        screen_comp = self.get_singleton_component(ScreenSingletonComponent)

        screen = screen_comp.screen
        bg_color = screen_comp.bg_color
        entities = self.get_required_entities()

        screen.fill(bg_color)
        for entity in entities:
            self._render_entity(screen, entity)
        self._render_selected_boxes(screen)
    
    def _render_selected_boxes(self, screen: pygame.Surface):
        draft_character_icons = self.get_entities_intersect([DraftCharacterComponent, CharacterButtonMarker])
        for entity in draft_character_icons:
            draft_char_comp = entity.get_component(DraftCharacterComponent)

            if draft_char_comp.banned:
                rect_comp = entity.get_component(RectangleVisualComponent)
                ui_comp = entity.get_component(UIComponent)
                
                dark_box = pygame.Surface(rect_comp.size)
                dark_box.set_alpha(128)
                dark_box.fill((50,0,0))

                screen.blit(dark_box, ui_comp.pos)
            
            
            

