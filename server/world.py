import pytmx
from singleton import SingletonMeta
from pytmx.util_pygame import load_pygame
from settings import *


class World(metaclass=SingletonMeta):
    def __init__(self):
        self.map = load_pygame("data/maps/map.tmx")

        entities_layer = self.map.get_layer_by_name("Entities")
        if entities_layer is not None and isinstance(entities_layer, pytmx.TiledObjectGroup):
            for obj in entities_layer:
                if obj.name == "PlayerSpawn":
                    self.player_spawn = (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR)