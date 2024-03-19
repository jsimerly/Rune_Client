import pygame
import os
from typing import Any, Literal
from dataclasses import dataclass

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

def load_image(*args):
    img_path = os.path.join(current_dir, *args)
    return pygame.image.load(img_path).convert_alpha()

def scale_image(img: pygame.Surface, size: tuple[int,int]):
    return pygame.transform.scale(img, size)

@dataclass
class CharacterInfo:
    display_name: str
    role: Literal['tank', 'support', 'damage']
    damage: int
    durability: int
    utility: int
    difficulty: int
    icon_image: pygame.Surface
    full_image: pygame.Surface

    cached_scaled_image: pygame.Surface | None = None

    def get_full_image(self, img_size: tuple[int, int]):
        if self.cached_scaled_image:
            return self.cached_scaled_image
        
        scaled_image = scale_image(self.full_image, img_size)
        self.cached_scaled_image = scaled_image
        return scaled_image

character_info: dict[int, CharacterInfo] = {
    1: CharacterInfo(
        display_name='Athlea',
        role='support',
        damage     =3,
        durability =6,
        utility    =6,
        difficulty =5,
        icon_image=load_image('assets', 'images', 'icons', 'athlea_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'athlea.png'),
    ),
    2: CharacterInfo(
        display_name= 'Bizi',
        role= 'support',
        damage     = 5,
        durability = 3,
        utility    = 7,
        difficulty = 8,
        icon_image= load_image('assets', 'images', 'icons', 'bizi_icon.png'),
        full_image= load_image('assets', 'images', 'full_character', 'bizi.png')
    ),
    3: CharacterInfo(
        display_name= 'Bolinda',
        role= 'damage',
        damage     = 9,
        durability = 3,
        utility    = 3,
        difficulty = 8,
        icon_image=load_image('assets', 'images', 'icons', 'bolinda_icon.png'),
        full_image= load_image('assets', 'images', 'full_character', 'bolinda.png')
    ),
    4: CharacterInfo(
        display_name= 'Crud',
        role= 'tank',
        damage     = 6,
        durability = 6,
        utility    = 3,
        difficulty = 3,
        icon_image= load_image('assets', 'images', 'icons', 'crud_icon.png'),
        full_image= load_image('assets', 'images', 'full_character', 'crud.png')
    ),
    5: CharacterInfo(
        display_name= 'Emily',
        role= 'support',
        damage     = 1,
        durability = 5,
        utility    = 9,
        difficulty = 3,
        icon_image=load_image('assets', 'images', 'icons', 'emily_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'emily.png'),

    ),
    6: CharacterInfo(
        display_name= 'Herc',
        role= 'tank',
        damage     = 7,
        durability = 5,
        utility    = 3,
        difficulty = 6,
        icon_image= load_image('assets', 'images', 'icons', 'herc_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'herc.png')
    ),
    7: CharacterInfo(
        display_name= 'Ivan',
        role= 'damage',
        damage     = 6,
        durability = 3,
        utility    = 6,
        difficulty = 6,
        icon_image=load_image('assets', 'images', 'icons', 'ivan_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'ivan.png')
    ),
    8: CharacterInfo(
        display_name= 'Judy',
        role= 'damage',
        damage     = 8,
        durability = 3,
        utility    = 4,
        difficulty = 5,
        icon_image=load_image('assets', 'images', 'icons', 'judy_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'judy.png')
    ),
    9: CharacterInfo(
        display_name= 'Kane',
        role= 'tank',
        damage     = 2,
        durability = 7,
        utility    = 6,
        difficulty = 4,
        icon_image=load_image('assets', 'images', 'icons', 'kane_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'kane.png')
    ),
    10: CharacterInfo(
        display_name= 'Lu',
        role= 'damage',
        damage     = 6,
        durability = 4,
        utility    = 5,
        difficulty = 6,
        icon_image=load_image('assets', 'images', 'icons', 'lu_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'lu.png')
    ),
    11: CharacterInfo(
        display_name= 'Navi',
        role= 'damage',
        damage     = 5,
        durability  = 5,
        utility    = 7,
        difficulty = 6,
        icon_image=load_image('assets', 'images', 'icons', 'navi_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'navi.png')
    ),
    12: CharacterInfo(
        display_name= 'Papa',
        role= 'damage',
        damage     = 5,
        durability = 5,
        utility    = 8,
        difficulty = 8,
        icon_image=load_image('assets', 'images', 'icons', 'papa_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'papa.png')
    ),
    13: CharacterInfo(
        display_name= 'Tim',
        role= 'damage',
        damage     = 10,
        durability = 1,
        utility    = 4,
        difficulty = 9,
        icon_image=load_image('assets', 'images', 'icons', 'tim_icon.png'),
        full_image=load_image('assets', 'images', 'full_character', 'tim.png')
    ),
}

@dataclass
class RoleInfo:
    display_name: str
    image: pygame.Surface
    cached_scaled_image: pygame.Surface | None = None

    def get_image(self, img_size: tuple[int, int]):
        if self.cached_scaled_image:
            return self.cached_scaled_image
        
        scaled_image = scale_image(self.image, img_size)
        self.cached_scaled_image = scaled_image
        return scaled_image

role_info: dict[str, RoleInfo] = {
    'tank': RoleInfo(
        display_name='Tank',
        image=load_image('assets', 'images', 'roles', 'tank_logo.webp')
    ),
    'support': RoleInfo(
        display_name='Support',
        image=load_image('assets', 'images', 'roles', 'support_logo.webp')
    ),
    'damage': RoleInfo(
        display_name='DPS',
        image=load_image('assets', 'images', 'roles', 'damage_logo.webp')
    ),
}