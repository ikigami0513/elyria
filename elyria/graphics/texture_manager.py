import pygame
from core.singleton import SingletonMeta
from typing import Dict, Optional


class TextureManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.textures: Dict[str, pygame.Surface] = {}

    def add_texture(self, name: str, path: str) -> pygame.Surface:
        if name not in self.textures:
            self.textures[name] = pygame.image.load(path).convert_alpha()
        return self.textures[name]
    
    def get_texture(self, name: str) -> Optional[pygame.Surface]:
        return self.textures.get(name)
