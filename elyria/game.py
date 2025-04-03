import sys
import json
import pygame
from texture_manager import TextureManager
from animation_manager import AnimationManager
from animation import Animation
from world import World
from settings import *
from typing import Dict, List, Union
from logger import logger


class Game:
    def __init__(self):
        pygame.init()

        logger.info(sys.version.replace("\n", " "))
        pygame_version = pygame.version.ver
        sdl_version = pygame.version.SDL.major, pygame.version.SDL.minor, pygame.version.SDL.patch
        python_version = ".".join(map(str, sys.version_info[:3]))
        version_string = f"pygame-ce {pygame_version} (SDL {'.'.join(map(str, sdl_version))}, Python {python_version})"
        logger.info(version_string)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"Elyria - 0 FPS")
        self.clock = pygame.time.Clock()
        self.running = True
        self.load()
        self.world = World()
        self.fps_update_time = 0

    def load(self):
        texture_manager = TextureManager()
        with open("data/textures.json", "r") as f:
            textures: List[Dict[str, str]] = json.load(f)

        for texture in textures:
            texture_manager.add_texture(texture["key"], texture["path"])
        logger.info(f"Textures loaded from data/textures.json file")

        animation_manager = AnimationManager()
        with open("data/animations.json", "r") as f:
            animations: List[Dict[str, Union[str, int]]] = json.load(f)

        for animation in animations:
            animation_manager.add_animation(
                animation["key"], 
                Animation(
                    texture_manager.get_texture(animation["texture"]), 
                    animation["width"], animation["height"], 
                    animation["row"], animation["frames"], 
                    animation["speed"]
                )
            )
        logger.info(f"Animations loaded from data/animations.json file")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        dt = self.clock.tick() / 1000.0

        self.fps_update_time += dt
        if self.fps_update_time >= 1:
            pygame.display.set_caption(f"Elyria - {int(self.clock.get_fps())} FPS")
            self.fps_update_time = 0

        self.world.update(dt)
        
    def draw(self):
        self.world.draw()
