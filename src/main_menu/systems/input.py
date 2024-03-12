from ecs_engine.system import System, subscribe_to_event
from src.main_menu.components.input_singleton import MenuInputSingletonComponent
import pygame

class InputSystem(System):
    @subscribe_to_event('pygame_events')
    def update(self, events: list[pygame.event.Event]):
        input_comp = self.get_singleton_component(MenuInputSingletonComponent)
        input_comp.events = events
        


        