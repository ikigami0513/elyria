import pygame
import pytmx
from player import Player
from settings import *
from sprites import Generic
from groups import CameraGroup
from texture_manager import TextureManager


class World:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.setup()

    def setup(self) -> None:
        map_data = pytmx.load_pygame("data/maps/map.tmx")

        # ground_layer = map_data.get_layer_by_name("Ground")
        # if ground_layer is not None and isinstance(ground_layer, pytmx.TiledTileLayer):
        #     for x, y, gid in ground_layer:
        #         tile = map_data.get_tile_image_by_gid(gid)
        #         if tile:
        #             Generic((x * TILE_SIZE * 2, y * TILE_SIZE * 2), pygame.transform.scale(tile, (TILE_SIZE * 2, TILE_SIZE * 2)), self.all_sprites)

        entities_layer = map_data.get_layer_by_name("Entities")
        if entities_layer is not None and isinstance(entities_layer, pytmx.TiledObjectGroup):
            for obj in entities_layer:
                if obj.name == "PlayerStart":
                    self.player = Player(pos=(obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR), groups=self.all_sprites, scale=(SCALE_FACTOR, SCALE_FACTOR))

        ground_texture = TextureManager().get_texture("ground_layer")
        Generic(
            pos=(0, 0),
            surf=pygame.transform.scale(ground_texture, (ground_texture.width * SCALE_FACTOR, ground_texture.height * SCALE_FACTOR)),
            groups=self.all_sprites,
            z=LAYERS["ground"]
        )

    def update(self, dt: float) -> None:
        self.player.update(dt)
        self.all_sprites.update(dt)

    def draw(self):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player)
        pygame.display.update()
        