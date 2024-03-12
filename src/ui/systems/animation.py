from ecs_engine import System, subscribe_to_event
from ecs_engine.entity_admin import EcsAdmin
from ecs_engine.interfaces import IEventBus
from src.ui.components.animation import UIAnimationComponent
from src.ui.systems.scripts import default_animation_scripts, AnimationFunction    
import pygame

class UIAnimationSystem(System):
    required_components = [UIAnimationComponent]
    default_animation_scripts = default_animation_scripts
    animation_scripts: dict[str, AnimationFunction] = {}

    def __init__(self, ecs_admin: EcsAdmin, event_bus: IEventBus):
        super().__init__(ecs_admin, event_bus)
        self.animation_scripts = self.animation_scripts | default_animation_scripts

    def update(self, dt: int):
        entities = self.get_required_entities()
        for entity in entities:
            animation_comp = entity.get_component(UIAnimationComponent)
            start_time = animation_comp.start_time
            current_time = pygame.time.get_ticks()
            time_elaspsed = current_time - start_time

            if animation_comp.duration_ms and time_elaspsed >= animation_comp.duration_ms:
                animation_comp.state = 'end'

            animation = self.animation_scripts[animation_comp.animation_id]
            animation(entity, animation_comp)

            if animation_comp.state == 'start':
                animation_comp.state = 'active'

            if animation_comp.state == 'end':
                self.remove_component(entity, animation_comp)
            