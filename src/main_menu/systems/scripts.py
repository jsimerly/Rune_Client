            
from src.ui.components.visual import TextVisualComponent
from src.ui.components.animation import UIAnimationComponent
from src.main_menu.components.match_making_singleton import MatchMakingSingletonComponent
from src.main_menu.components.markers import MainMenuButtonMarker
from ecs_engine import  Entity
from src.utility.sizing import calculate_component_text_pos
from datetime import datetime
import pygame

def blinking_in_queue(entity: Entity, animation_comp: UIAnimationComponent):
    text_comp = entity.get_component(TextVisualComponent)
    if animation_comp.state == 'start':
        text = 'Start Game'

    if animation_comp.state == 'active':
        elapsed_time = pygame.time.get_ticks() - animation_comp.start_time
        seconds_elapsed = elapsed_time // 1000
        dots_count = int(seconds_elapsed) % 3
        text = 'Cancel.' + '.' * dots_count

    if animation_comp.state == 'end':
        text = 'Start Game'

    text_comp.text = text
    pos = calculate_component_text_pos(entity)
    text_comp.pos = pos
        