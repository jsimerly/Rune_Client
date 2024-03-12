from src.ui.systems.animation import UIAnimationSystem
from src.main_menu.components.markers import MainMenuButtonMarker
from src.main_menu.components.match_making_singleton import MatchMakingSingletonComponent
from src.main_menu.systems.scripts import blinking_in_queue
from ecs_engine import subscribe_to_event


class MainMenuUIAnimationSystem(UIAnimationSystem):
    animation_scripts = {'blinking_in_queue': blinking_in_queue}

    @subscribe_to_event('update_dt')
    def update(self, dt: int):
        super().update(dt)
        


