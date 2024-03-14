import pygame
import os

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

def load_image(*args):
    img_path = os.path.join(current_dir, *args)
    return pygame.image.load(img_path).convert_alpha()

character_icons: dict[int, pygame.Surface] = {
    1: load_image('assets', 'images', 'icons', 'athlea_icon.png'), # Athlea
    2: load_image('assets', 'images', 'icons', 'bizi_icon.png'),    # Bizi
    3: load_image('assets', 'images', 'icons', 'bolinda_icon.png'), # Bolinda
    4: load_image('assets', 'images', 'icons', 'crud_icon.png'),    # Crud
    5: load_image('assets', 'images', 'icons', 'emily_icon.png'),   # Emily
    6: load_image('assets', 'images', 'icons', 'herc_icon.png'),    # Herc
    7: load_image('assets', 'images', 'icons', 'ivan_icon.png'),    # Ivan
    8: load_image('assets', 'images', 'icons', 'judy_icon.png'),    # Judy
    9: load_image('assets', 'images', 'icons', 'kane_icon.png'),    # Kane
    10: load_image('assets', 'images', 'icons', 'lu_icon.png'),     # Lu
    11: load_image('assets', 'images', 'icons', 'navi_icon.png'),   # Navi
    12: load_image('assets', 'images', 'icons', 'papa_icon.png'),   # Papa
    13: load_image('assets', 'images', 'icons', 'tim_icon.png'),    # Tim
}

character_full_image: dict[int, pygame.Surface] = {
    1: load_image('assets', 'images', 'full_character', 'athlea.png'),  # Athlea
    2: load_image('assets', 'images', 'full_character', 'bizi.png'),    # Bizi
    3: load_image('assets', 'images', 'full_character', 'bolinda.png'), # Bolinda
    4: load_image('assets', 'images', 'full_character', 'crud.png'),    # Crud
    5: load_image('assets', 'images', 'full_character', 'emily.png'),   # Emily
    6: load_image('assets', 'images', 'full_character', 'herc.png'),    # Herc
    7: load_image('assets', 'images', 'full_character', 'ivan.png'),    # Ivan
    8: load_image('assets', 'images', 'full_character', 'judy.png'),    # Judy
    9: load_image('assets', 'images', 'full_character', 'kane.png'),    # Kane
    10: load_image('assets', 'images', 'full_character', 'lu.png'),     # Lu
    11: load_image('assets', 'images', 'full_character', 'navi.png'),   # Navi
    12: load_image('assets', 'images', 'full_character', 'papa.png'),   # Papa
    13: load_image('assets', 'images', 'full_character', 'tim.png'),    # Tim
}