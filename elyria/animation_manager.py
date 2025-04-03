import pygame
from animation import Animation
from singleton import SingletonMeta
from typing import Dict, Optional


class AnimationManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.animations: Dict[str, Animation] = {}

    def add_animation(self, name: str, animation: Animation) -> Animation:
        if name not in self.animations:
            self.animations[name] = animation
        return self.animations[name]
    
    def get_animation(self, name: str) -> Optional[Animation]:
        animation = self.animations.get(name)
        if not animation:
            return None
        
        return Animation(
            texture=animation.texture,
            width=animation.width,
            height=animation.height,
            row=animation.row,
            frames=animation.frames,
            animation_speed=animation.animation_speed
        )
    