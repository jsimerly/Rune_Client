import pygame
import logging
logging.basicConfig(level=logging.INFO)  # Adjust the logging level as needed
logger = logging.getLogger(__name__)

class FontManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FontManager, cls).__new__(cls)
            cls._instance.init(*args, **kwargs)
        return cls._instance
    
    def init(self):
        pygame.font.init()
        self.fonts: dict[str, dict[int, pygame.font.Font]] = {'std': {}}

    def get_font(self, font_path: str | None, size: int) -> pygame.font.Font:
        if font_path is None:
            fonts = self.fonts['std']
            return self._get_font_size(size, fonts)
        
        if font_path not in self.fonts:
            try:
                font = pygame.font.Font(font_path, size)
                self.fonts[font_path] = font
                return font
                
            except Exception as e:
                logger.error(f"Failed to load font from {font_path}: {e}")
                return self._get_font_size(size, self.fonts['std'])
    
    def _get_font_size(self, size: int, fonts: dict[int, pygame.font.Font]) -> pygame.font.Font:
        if size not in fonts:
            fonts[size] = pygame.font.Font(None, size)
        return fonts[size]
    

    

            
    
