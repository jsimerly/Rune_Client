from client_state import ClientState
from network import NetworkManager
from dataclasses import dataclass
import pygame
from main_menu.main_menu import MainMenu

class Client:
    def __init__(self) -> None:
        pygame.init()
        self.client_state = ClientState()
        self.network = NetworkManager()
        # self.network.start_listening()

        game_states = {
            'main_menu': MainMenu(),
            'drafting': self.drafting,
            'in_game': self.in_game
        }
    
        self.client_state.set_game_states(game_states, 'main_menu')

    def main_menu(self):
        ...

    def drafting(self):
        ...

    def in_game(self):
        ...

    def run(self):
        while self.client_state.is_running:
            self.client_state.state.update()
        pygame.quit()


if __name__ == '__main__':
    client = Client()
    client.run()
