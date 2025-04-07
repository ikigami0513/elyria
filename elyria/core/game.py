import sys
import json
import pygame
from core.singleton import SingletonMeta
from graphics.texture_manager import TextureManager
from graphics.animation_manager import AnimationManager
from graphics.animation import Animation
from world.world import World
from core.settings import *
from typing import Dict, List, Union
from core.logger import logger
from core.utils import resource_path
from threading import Thread
from network.gameclient import start_twisted


class Game(metaclass=SingletonMeta):
    def __init__(self):
        success, failure = pygame.init()

        logger.info(sys.version.replace("\n", " "))
        pygame_version = pygame.version.ver
        sdl_version = pygame.version.SDL.major, pygame.version.SDL.minor, pygame.version.SDL.patch
        python_version = ".".join(map(str, sys.version_info[:3]))
        version_string = f"pygame-ce {pygame_version} (SDL {'.'.join(map(str, sdl_version))}, Python {python_version})"
        logger.info(version_string)

        logger.info(f"{success} modules loaded successfully, {failure} modules could not be loaded")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(f"Elyria - 0 FPS")
        self.clock = pygame.time.Clock()
        self.running = True
        self.load()
        self.world = World()
        self.fps_update_time = 0

        Thread(target=start_twisted, daemon=True).start()

    def load(self):
        texture_manager = TextureManager()
        for file in TEXTURES_FILES:
            with open(resource_path(file), "r") as f:
                textures: List[Dict[str, str]] = json.load(f)

            for texture in textures:
                texture_manager.add_texture(texture["key"], resource_path(texture["path"]))
            logger.info(f"Textures loaded from {file} file.")

        animation_manager = AnimationManager()
        for file in ANIMATIONS_FILES:
            with open(resource_path(file), "r") as f:
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
            logger.info(f"Animations loaded from {file} file.")

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
            elif event.type == pygame.VIDEORESIZE:
                self.on_resize(event.w, event.h)

    def on_resize(self, width: int, height: int):
        self.world.all_sprites.set_half(width, height)
        for ui_element in self.world.ui_layer.sprites():
            if hasattr(ui_element, "on_window_resize"):
                ui_element.on_window_resize(width, height)
        
        logger.info(f"Window resized to {width}x{height}")

    def update(self):
        dt = self.clock.tick() / 1000.0

        self.fps_update_time += dt
        if self.fps_update_time >= 1:
            pygame.display.set_caption(f"Elyria - {int(self.clock.get_fps())} FPS")
            self.fps_update_time = 0

        self.world.update(dt)
        
    def draw(self):
        self.world.draw()
