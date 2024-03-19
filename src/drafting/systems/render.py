from ecs_engine.entity_admin import EcsAdmin
from ecs_engine.interfaces import IEventBus
from src.ui.systems.render_ui import RenderUISystem
from src.drafting.components.character import DraftCharacterComponent, SelectedCharacterSingleton
from src.drafting.components.markers import CharacterButtonMarker
from src.drafting.components.draft_state import DraftStateSingletonComponent
from src.ui.components.visual import RectangleVisualComponent, UIComponent
from src.global_singleton_comps import ScreenSingletonComponent
from src.drafting.characters import character_info, role_info
import pygame
from ecs_engine import subscribe_to_event

class DraftRenderUISystem(RenderUISystem):
    font = pygame.font.SysFont(None, 26)
    large_font = pygame.font.SysFont(None, 44)

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
        self._render_character_preview(screen)
    
    def _render_selected_boxes(self, screen: pygame.Surface):
        draft_character_icons = self.get_entities_intersect([CharacterButtonMarker])
        draft_state = self.get_singleton_component(DraftStateSingletonComponent)
        selected_char = self.get_singleton_component(SelectedCharacterSingleton)

        for entity in draft_character_icons:
            draft_char_comp = entity.get_component(CharacterButtonMarker)
            if selected_char.char_id == draft_char_comp.char_id:
                rect_comp = entity.get_component(RectangleVisualComponent)
                ui_comp = entity.get_component(UIComponent)

                rect = pygame.Rect(ui_comp.pos, rect_comp.size)
                pygame.draw.rect(screen, (255, 225, 255), rect, 5, border_radius=rect_comp.attributes['radius'])

            if draft_char_comp.char_id not in draft_state.available_picks:
                rect_comp = entity.get_component(RectangleVisualComponent)
                ui_comp = entity.get_component(UIComponent)

                dark_box = pygame.Surface(rect_comp.size)
                dark_box.set_alpha(128)
                dark_box.fill((0,0,0))

                screen.blit(dark_box, ui_comp.pos)

    def _render_character_preview(self, screen: pygame.Surface):
        selected_char_comp = self.get_singleton_component(SelectedCharacterSingleton)
        if selected_char_comp.char_id:
            screen_size = screen.get_size()
            selected_char_info = character_info[selected_char_comp.char_id]

            image_size = (screen_size[0] * .25, screen_size[0] * .25)
            image_pos = (screen_size[0] * .175, screen_size[1] * .1)

            full_image = selected_char_info.get_full_image(image_size)
            screen.blit(full_image, image_pos)

            start_pos_info = (image_pos[0] + image_size[0] + 5, image_pos[1] + image_size[1] + 5)
            selected_char_role = role_info[selected_char_info.role]

            selected_role_image_size = (screen_size[0] * .075, screen_size[0] * .075)
            selected_role_image_pos = (start_pos_info[0], start_pos_info[1] - selected_role_image_size[1] - 5)
            select_role_image = selected_char_role.get_image(selected_role_image_size)

            screen.blit(select_role_image, selected_role_image_pos)

            role_text_surface = self.font.render(selected_char_role.display_name, True, (225,225,255))
            text_size = self.font.size(selected_char_role.display_name)
            role_text_pos = (
                selected_role_image_pos[0] + selected_role_image_size[0]//2 - text_size[0]//2,
                selected_role_image_pos[1] + selected_role_image_size[1] + 5,
            )
            screen.blit(role_text_surface, role_text_pos)

            char_name = selected_char_info.display_name
            char_name_surface = self.large_font.render(char_name, True, (255, 255, 255))
            char_name_pos = (
                image_size[0] + image_pos[0] + 5, 
                screen_size[1] * .1
            )
            screen.blit(char_name_surface, char_name_pos)

            
            start_x = selected_role_image_pos[0] + selected_role_image_size[0] + 5
            start_y = selected_role_image_pos[1]
            end_x = screen_size[0] * .825 # (1-.175)
            end_y = start_y + selected_role_image_size[1] + text_size[1]

            box_size = (
                (end_x - start_x)//2 - 2,
                (end_y - start_y)//2 - 2
            )     
            
            def box_perc(val: int):
                return .33 + (val/10)*(.67)
      
            damage_pos = (start_x, start_y)
            damage_size = (box_size[0] * box_perc(selected_char_info.damage), box_size[1])
            damage_rect = pygame.Rect(damage_pos, damage_size)

            durablity_pos = (start_x, start_y + box_size[1] + 4)
            durability_size = (box_size[0] * box_perc(selected_char_info.durability), box_size[1])
            durability_rect = pygame.Rect(durablity_pos, durability_size)

            
            utility_size = (box_size[0] * box_perc(selected_char_info.utility), box_size[1])
            utility_pos = (start_x + box_size[0] + 4, start_y)
            utility_rect = pygame.Rect(utility_pos, utility_size)

            difficulty_size   = (box_size[0] * box_perc(selected_char_info.difficulty), box_size[1])
            difficulty_pos = (start_x + box_size[0] + 4, start_y + box_size[1] + 4)
            difficulty_rect = pygame.Rect(difficulty_pos, difficulty_size)
            
            self._create_stat_box(screen, 'Damage', (115, 11, 0), damage_rect)
            self._create_stat_box(screen, 'Durability', (1, 77, 2), durability_rect)
            self._create_stat_box(screen, 'Utility', (100, 2, 115), utility_rect)
            self._create_stat_box(screen, 'Difficulity', (100, 170, 202), difficulty_rect)
    
    def _create_stat_box(self, screen: pygame.Surface, text: str, color: tuple[int,int,int], rect: pygame.Rect):
        pygame.draw.rect(screen, color, rect, border_radius=5)

        text_surface = self.font.render(text, True, (255, 255, 255))
        text_pos = (rect.left + 5, (rect.height - self.font.size(text)[1])//2 + rect.top)
        screen.blit(text_surface, text_pos)





            



            


            

            
            
            
            

