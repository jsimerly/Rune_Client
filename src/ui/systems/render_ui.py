from __future__ import annotations
from ecs_engine import System
from ecs_engine.system import subscribe_to_event
from typing import TYPE_CHECKING
from src.global_singleton_comps import ScreenSingletonComponent
from src.ui.components.visual import RectangleVisualComponent, TextVisualComponent, ImageComponent, UIComponent
from src.main_menu.components.match_making_singleton import MatchMakingSingletonComponent
from src.main_menu.components.markers import MainMenuButtonMarker
from src.utility.sizing import  calculate_component_text_pos
from datetime import datetime
import pygame

if TYPE_CHECKING:
    from ecs_engine import Entity

class RenderUISystem(System):
    required_components = [UIComponent]

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
        ui_comp = entity.get_component(UIComponent)

        rect_comp = entity.get_component(RectangleVisualComponent)
        text_comp = entity.get_component(TextVisualComponent)
        image_comp = entity.get_component(ImageComponent)

        self._render_rect_comp(
            screen, entity, ui_comp, rect_comp, text_comp, image_comp
        )

    def _render_rect_comp(self, 
            screen: pygame. Surface,
            entity: Entity,
            ui_comp: UIComponent | None, 
            rect_comp: RectangleVisualComponent | None, text_comp: TextVisualComponent | None, 
            image_comp: ImageComponent | None
        ):

        in_focus = ui_comp.in_focus

        if rect_comp:
            rect = pygame.Rect(ui_comp.pos, rect_comp.size)
            rect_active_attr = rect_comp.focus_attributes if in_focus else rect_comp.attributes
            
            # Background
            if 'bg_color' in rect_active_attr and rect_active_attr['bg_color']:
                color = rect_active_attr['bg_color']
                radius = rect_active_attr.get('radius', 0)  # Use default value if 'radius' key is missing
                pygame.draw.rect(screen, color, rect, border_radius=radius)

        if image_comp:
            screen.blit(image_comp.image, image_comp.pos)

        # Outline
        if rect_comp:
            rect = pygame.Rect(ui_comp.pos, rect_comp.size)
            rect_active_attr = rect_comp.focus_attributes if in_focus else rect_comp.attributes

            if 'border_thickness' in rect_active_attr and rect_active_attr['border_thickness'] > 0:
                thickness = rect_active_attr['border_thickness']
                color = rect_active_attr['border_color']
                radius = rect_active_attr.get('radius', 0)
                pygame.draw.rect(screen, color, rect, thickness, border_radius=radius)

        if text_comp:
            text = text_comp.text
            pos = text_comp.pos
            text_surface = text_comp.attributes['font'].render(
                text, 
                True,
                text_comp.attributes['color']
            )
            screen.blit(text_surface, pos)