import pygame
from player import Player
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

    def draw(self, player: Player):
        self.offset.x = player.entities["player_base"].rect.centerx - self.half_width
        self.offset.y = player.entities["player_base"].rect.centery - self.half_height

        screen_rect = self.display_surface.get_rect()

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    if screen_rect.colliderect(offset_rect):
                        self.display_surface.blit(sprite.image, offset_rect)
