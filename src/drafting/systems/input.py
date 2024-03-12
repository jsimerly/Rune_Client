from ecs_engine.system import System, subscribe_to_event
from src.drafting.components.input_singleton import DraftInputSingletonComponent
import pygame

class InputSystem(System):
    @subscribe_to_event('pygame_events')
    def update(self, events: list[pygame.event.Event]):
        input_comp = self.get_singleton_component(DraftInputSingletonComponent)
        input_comp.events = events
        