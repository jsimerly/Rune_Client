from __future__ import annotations
from ecs_engine import System
from ecs_engine.system import subscribe_to_event
from typing import TYPE_CHECKING
from main_menu.components.screen_singleton import ScreenSingletonComponent
from ui.components.visual import RectangleVisualComponent, TextVisualComponent, ImageComponent, UIPositionComponent
from main_menu.components.markers import LfgButtonMarker
from main_menu.components.match_making_singleton import MatchMakingSingletonComponent
import pygame
from ui.font_singleton import FontManager
from utility.sizing import calculate_component_pos_rect, calculate_component_text_pos
from datetime import datetime

if TYPE_CHECKING:
    from ecs_engine import Entity

class RenderUISystem(System):
    required_components = [UIPositionComponent]

    @subscribe_to_event('update_dt')
    def update(self, dt: int):
        screen_comp = self.get_singleton_component(ScreenSingletonComponent)

        screen = screen_comp.screen
        bg_color = screen_comp.bg_color
        entities = self.get_required_entities()

        screen.fill(bg_color)
        for entity in entities:
            self._render_entity(screen, entity)

    def _render_entity(self, screen: pygame.Surface, entity: Entity):
        pos_comp = entity.get_component(UIPositionComponent)

        rect_comp = entity.get_component(RectangleVisualComponent)
        text_comp = entity.get_component(TextVisualComponent)
        image_comp = entity.get_component(ImageComponent)

        self._render_rect_comp(
            screen, entity, pos_comp, rect_comp, text_comp, image_comp
        )

    def _render_rect_comp(self, 
            screen: pygame. Surface,
            entity: Entity,
            pos_comp: UIPositionComponent | None, 
            rect_comp: RectangleVisualComponent | None, 
            text_comp: TextVisualComponent | None, 
            image_comp: ImageComponent | None
        ):
        if rect_comp:
            rect = pygame.Rect(pos_comp.pos, rect_comp.size)
            # Background
            if rect_comp.attributes['bg_color']:
                color = rect_comp.attributes['bg_color']
                radius = rect_comp.attributes['radius']
                pygame.draw.rect(screen, color, rect, border_radius=radius)

            # Outline
            if rect_comp.attributes['border_thickness'] > 0:
                thickness = rect_comp.attributes['border_thickness']
                color = rect_comp.attributes['border_color']
                radius = rect_comp.attributes['radius']
                pygame.draw.rect(screen, color, rect, thickness, radius)

            if image_comp:
                screen.blit(image_comp.image, image_comp.pos)

            if text_comp:
                text = text_comp.text
                pos = text_comp.pos
                if entity.has_component(LfgButtonMarker):
                    match_making_comp = self.get_singleton_component(MatchMakingSingletonComponent)
                    if match_making_comp.looking_for_game:
                        elapsed = datetime.now() - match_making_comp.start_queue_time
                        seconds_elapsed = elapsed.total_seconds()
                        dots_count = int(seconds_elapsed) % 3
                        text_comp.text = 'Cancel.' + '.' * dots_count
                    else:
                        text = 'Start Game'
    
                    pos = calculate_component_text_pos(entity)

                text_surface = text_comp.attributes['font'].render(
                    text, 
                    True,
                    text_comp.attributes['color']
                )
                screen.blit(text_surface, pos)
