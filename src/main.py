from src.client_state import ClientState
from src.network import NetworkManager
from src.main_menu.main_menu import MainMenu
from src.drafting.drafting import Drafting
import pygame

class Client:
    def __init__(self) -> None:
        pygame.init()
        self.client_state = ClientState()
        self.network = NetworkManager()
        self.network.connect()

        # block here

        game_states = {
            'main_menu': MainMenu(),
            'draft': Drafting(),
            'in_game': ...
        }
    
        self.client_state.set_game_states(game_states)
        self.client_state.update_state('main_menu')

    def run(self):
        while self.client_state.is_running:
            self.client_state.state.update()
        self.network.close_connection()
        pygame.quit()
        
if __name__ == '__main__':
    client = Client()
    client.run()
