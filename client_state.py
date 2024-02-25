import json
from interfaces import AbstractClientState


DEFAULT_SCREEN_SIZE = (800, 600)
DEFAULT_FPS = 60

class ClientState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ClientState, cls).__new__(cls)
            cls._instance.init(*args, **kwargs)
        return cls._instance

    def init(self) -> None:
        self.states = {}
        self.state = None

        self.screen_size = None
        self.fps = None
        
        self.load_user_settings('user_settings.json')
        self.is_running = True

    def set_game_states(self, states: dict[str, AbstractClientState], starting_state: str):
        self.states = states
        self.state = states[starting_state]

    def update_state(self, state_name: str):
        self.state = self.states[state_name]

    def load_user_settings(self, filename: str):
        try:
            with open(filename, 'r') as f:
                settings= json.load(f)
                self.set_screen_size(settings["screen_size"])
                self.set_fps(settings['fps'])
        except:
            self.screen_size = DEFAULT_SCREEN_SIZE
            self.fps = DEFAULT_FPS

    def set_screen_size(self, screen_size: list[int,int]):
        if isinstance(screen_size, list) and len(screen_size) == 2:
            self.screen_size = tuple(screen_size)
            return
        self.screen_size = DEFAULT_SCREEN_SIZE

    def set_fps(self, fps: int):
        if isinstance(fps, int):
            self.fps = fps
            return
        self.fps = DEFAULT_FPS

    def close(self):
        self.is_running = False
