from ecs_engine.system import System, subscribe_to_event
from main_menu.components.match_making_singleton import MatchMakingSingletonComponent
from ui.components.visual import TextVisualComponent
from utility.sizing import calculate_component_text_pos
from datetime import datetime
import pygame

class LookForGame(System):
    @subscribe_to_event('look_for_game_click')
    def update(self):
        match_making_comp = self.get_singleton_component(MatchMakingSingletonComponent)
        match_making_button = self.get_entity(match_making_comp.start_match_button_id)
        text_comp = match_making_button.get_component(TextVisualComponent)
        
        if not match_making_comp.looking_for_game:
            match_making_comp.looking_for_game = True
            match_making_comp.start_queue_time = datetime.now()
        else:
            match_making_comp.looking_for_game = False

        text_comp.pos = calculate_component_text_pos(match_making_button)


        