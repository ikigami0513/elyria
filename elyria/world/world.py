import pygame
import pytmx
from entities.player import Player
from core.settings import *
from graphics.sprites import Generic
from world.groups import CameraGroup
from graphics.texture_manager import TextureManager
from core.utils import resource_path
from network.gameclient import GameClient


class World:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.ui_layer = pygame.sprite.Group()
        self.player = None
        self.setup()

    def setup(self) -> None:
        map_data = pytmx.load_pygame(resource_path("data/maps/map.tmx"))

        collision_layer = map_data.get_layer_by_name("Collisions")
        if collision_layer is not None and isinstance(collision_layer, pytmx.TiledTileLayer):
            for x, y, gid in collision_layer:
                tile = map_data.get_tile_image_by_gid(gid)
                if tile:
                    Generic(
                        pos=(x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR), 
                        surf=pygame.Surface((TILE_SIZE * SCALE_FACTOR, TILE_SIZE * SCALE_FACTOR)),
                        groups=self.collision_sprites
                    )

        ground_texture = TextureManager().get_texture("ground_layer")
        Generic(
            pos=(0, 0),
            surf=pygame.transform.scale(ground_texture, (ground_texture.width * SCALE_FACTOR, ground_texture.height * SCALE_FACTOR)),
            groups=self.all_sprites,
            z=LAYERS["ground"]
        )

    def update(self, dt: float) -> None:
        self.ui_layer.update(dt)
        if self.player:
            self.player.update(dt)
        self.all_sprites.update(dt)

    def draw(self):
        self.display_surface.fill('black')
        if self.player:
            self.all_sprites.draw(self.player)
        self.ui_layer.draw(self.display_surface)
        pygame.display.update()
        