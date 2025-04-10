import pygame
from entities.entity import Entity
from graphics.animation_manager import AnimationManager
from ui.hotbar import Hotbar
from typing import Tuple, Dict
from enum import Enum
from core.settings import *
from network.gameclient import GameClient


class Direction(Enum):
    DOWN = "down"
    RIGHT = "right"
    UP = "up"
    LEFT = "left"


class State(Enum):
    IDLE = "idle"
    WALK = "walk"


class Player:
    def __init__(self, pos: Tuple[int, int], groups: Tuple[pygame.sprite.Group], collision_sprites: pygame.sprite.Group, ui_layer: pygame.sprite.Group, is_local: bool, scale: Tuple[int, int] = (1.0, 1.0)):
        self.pos = pygame.math.Vector2(pos)
        self.groups = groups
        self.collision_sprites = collision_sprites
        self.scale = scale
        self.direction_vector = pygame.math.Vector2()
        self.speed = 200
        self.direction = Direction.DOWN
        self.state = State.IDLE
        self.animation_manager = AnimationManager()
        self.entities: Dict[str, Entity] = {
            "player_base": Entity(self.pos, self.animation_manager.get_animation(f"player_base_{self.state.value}_{self.direction.value}"), self.groups, self.scale),
            "player_medium_hair_brown": Entity(self.pos, self.animation_manager.get_animation(f"player_medium_hair_brown_{self.state.value}_{self.direction.value}"), self.groups, self.scale),
            "player_shirt_green": Entity(self.pos, self.animation_manager.get_animation(f"player_shirt_green_{self.state.value}_{self.direction.value}"), self.groups, self.scale),
            "player_hand": Entity(self.pos, self.animation_manager.get_animation(f"player_hand_{self.state.value}_{self.direction.value}"), self.groups, self.scale),
        }
        self.body = self.entities["player_base"]

        # networking
        self.is_local = is_local
        self.last_sent_position = self.pos.copy()
        self.send_cooldown = 0.05  # 20 fois par seconde (20 ticks)
        self.send_timer = 0.0

        # gui
        # usefull only if local player
        if self.is_local:
            self.ui_layer = ui_layer
            self.hotbar = Hotbar(
                texture_name="ui_premade",
                groups=self.ui_layer
            )

    def input(self):
        if self.is_local:
            keys = pygame.key.get_pressed()
            new_direction = self.direction
            new_state = State.IDLE

            if keys[pygame.K_z]:
                self.direction_vector.y = -1
                new_direction = Direction.UP
                new_state = State.WALK
            elif keys[pygame.K_s]:
                self.direction_vector.y = 1
                new_direction = Direction.DOWN
                new_state = State.WALK
            else:
                self.direction_vector.y = 0

            if keys[pygame.K_d]:
                self.direction_vector.x = 1
                new_direction = Direction.RIGHT
                new_state = State.WALK
            elif keys[pygame.K_q]:
                self.direction_vector.x = -1
                new_direction = Direction.LEFT
                new_state = State.WALK
            else:
                self.direction_vector.x = 0

            if new_direction != self.direction or new_state != self.state:
                self.direction = new_direction
                self.state = new_state
                for key, entity in self.entities.items():
                    entity.animation = self.animation_manager.get_animation(f"{key}_{self.state.value}_{self.direction.value}")

    def move(self, dt: float):
        if self.direction_vector.magnitude() > 0:
            self.direction_vector = self.direction_vector.normalize()

        self.pos.x += self.direction_vector.x * self.speed * dt
        self.set_pos_x(self.pos.x)
        self.collision("horizontal")

        self.pos.y += self.direction_vector.y * self.speed * dt
        self.set_pos_y(self.pos.y)
        self.collision("vertical")

        # Envoyer seulement si on bouge et que timer écoulé
        if self.direction_vector.length_squared() > 0:
            self.send_timer += dt
            if self.send_timer >= self.send_cooldown:
                self.send_timer = 0
                if self.pos.distance_to(self.last_sent_position) > 1.0:
                    GameClient().send_message("move", {
                        "position": {
                            "x": self.pos.x,
                            "y": self.pos.y
                        }
                    })
                    self.last_sent_position = self.pos.copy()

    def set_pos_x(self, x: float):
        for entity in self.entities.values():
            entity.pos.x = x
            entity.hitbox.centerx = x
            entity.rect.centerx = x

    def set_pos_y(self, y: float):
        for entity in self.entities.values():
            entity.pos.y = y
            entity.hitbox.centery = y
            entity.rect.centery = y

    def collision(self, direction: str):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "hitbox"):
                if sprite.hitbox.colliderect(self.body.hitbox):
                    if direction == "horizontal":
                        if self.direction_vector.x > 0:
                            self.body.hitbox.right = sprite.hitbox.left
                            self.pos.x = self.body.hitbox.centerx
                        if self.direction_vector.x < 0:
                            self.body.hitbox.left = sprite.hitbox.right
                            self.pos.x = self.body.hitbox.centerx
                        self.set_pos_x(self.pos.x)

                    if direction == "vertical":
                        if self.direction_vector.y > 0:
                            self.body.hitbox.bottom = sprite.hitbox.top
                            self.pos.y = self.body.hitbox.centery
                        if self.direction_vector.y < 0:
                            self.body.hitbox.top = sprite.hitbox.bottom
                            self.pos.y = self.body.hitbox.centery
                        self.set_pos_y(self.pos.y)

    def update(self, dt: float):
        self.input()
        self.move(dt)
        for entity in self.entities.values():
            entity.update(dt)
