from ecs_engine import SingletonComponent
from dataclasses import dataclass, field
import pygame
from datetime import datetime

@dataclass
class MatchMakingSingletonComponent(SingletonComponent):
    looking_for_game: bool = field(default=False)
    start_queue_time: datetime = field(default=datetime.now())
    start_match_button_id: int = field(default=None)
