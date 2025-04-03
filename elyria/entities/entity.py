import pygame
from graphics.animation import Animation
from core.settings import *
from typing import Tuple


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], animation: Animation, groups: Tuple[pygame.sprite.Group], scale: Tuple[int, int] = (1.0, 1.0), z: int = LAYERS["main"]):
        super().__init__(groups)
        self.animation = animation
        self.image = self.animation.get_frame()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.scale = pygame.math.Vector2(scale)
        self.z = z

    def update(self, dt: float) -> None:
        self.animation.update(dt)
        self.image = self.animation.get_frame()
        self.image = pygame.transform.scale(self.image, (self.image.width * self.scale.x, self.image.height * self.scale.y))
        self.rect = self.image.get_rect(center=self.pos)
