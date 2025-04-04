import pygame
from graphics.texture_manager import TextureManager
from typing import Tuple
from core.settings import *

class Hotbar(pygame.sprite.Sprite):
    def __init__(self, texture_name: str, groups: Tuple[pygame.sprite.Group]):
        super().__init__(groups)
        self.image = TextureManager().get_texture(texture_name)
        self.image = self.image.subsurface(pygame.Rect(
            (108, 154),
            (120, 28)
        ))
        self.image = pygame.transform.scale(self.image, (self.image.width * SCALE_FACTOR, self.image.height * SCALE_FACTOR))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    def on_window_resize(self, width: int, height: int):
        self.rect.center = (width // 2, height - 50)
