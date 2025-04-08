import pygame
import pytmx
from singleton import SingletonMeta
from sprites import Generic
from player import Player
from pytmx.util_pygame import load_pygame
from settings import *
from typing import Dict


class World(metaclass=SingletonMeta):
    def __init__(self):
        self.map = load_pygame("data/maps/map.tmx")
        self.players: Dict[int, Player] = {}
        self.player_group = pygame.sprite.Group()

        entities_layer = self.map.get_layer_by_name("Entities")
        if entities_layer is not None and isinstance(entities_layer, pytmx.TiledObjectGroup):
            for obj in entities_layer:
                if obj.name == "PlayerSpawn":
                    self.player_spawn = pygame.math.Vector2(obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR)
                    
        self.collision_sprites = pygame.sprite.Group()
        collision_layer = self.map.get_layer_by_name("Collisions")
        if collision_layer is not None and isinstance(collision_layer, pytmx.TiledTileLayer):
            for x, y, gid in collision_layer:
                tile = self.map.get_tile_image_by_gid(gid)
                if tile:
                    Generic(
                        pos=(x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR),
                        surf=pygame.Surface((TILE_SIZE * SCALE_FACTOR, TILE_SIZE * SCALE_FACTOR)),
                        groups=self.collision_sprites
                    )
