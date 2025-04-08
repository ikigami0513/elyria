import pickle
import pygame
from twisted.internet import tcp
from enum import Enum
from typing import Optional, Dict, Any, Tuple
from settings import *


class Direction(Enum):
    DOWN = "down"
    RIGHT = "right"
    UP = "up"
    LEFT = "left"


class State(Enum):
    IDLE = "idle"
    WALK = "walk"


class Player(pygame.sprite.Sprite):
    def __init__(self, player_id: int, transport: tcp.Server, position: pygame.math.Vector2, groups: Tuple[pygame.sprite.Group] = []):
        super().__init__(groups)
        self.id = player_id
        self.position = position
        self.image = pygame.Surface((PLAYER_SIZE.x * SCALE_FACTOR, PLAYER_SIZE.y * SCALE_FACTOR))
        self.rect = self.image.get_rect(center=self.position)
        self.transport = transport
        self.state = State.IDLE
        self.direction = Direction.DOWN
        self.direction_vector = pygame.math.Vector2()
        self.speed = 200

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "position": {
                "x": self.position.x,
                "y": self.position.y
            }
        }
    
    @classmethod
    def load(cls, player_id, transport: tcp.Server, groups: Tuple[pygame.sprite.Group] = []) -> Optional['Player']:
        try:
            with open(f"server/data/players/{player_id}.pkl", "rb") as f:
                data = pickle.load(f)

            position = pygame.math.Vector2(data["position"]["x"], data["position"]["y"])
            player = Player(player_id, transport, position, groups)

            return player
        except FileNotFoundError:
            print(f"The file for player {player_id} does not exist.")
            return None
        except Exception as e:
            print(f"Error loading player {player_id}: {e}")
            return None

    def save(self) -> None:
        with open(f"server/data/players/{self.id}.pkl", "wb") as f:
            pickle.dump(self.serialize(), f)
