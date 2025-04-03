import pygame


class Animation:
    def __init__(self, texture: pygame.Surface, width: int, height: int, row: int, frames: int, animation_speed: int):
        self.texture = texture
        self.width = width
        self.height = height
        self.row = row
        self.frames = frames
        self.animation_speed = animation_speed
        self.current_frame = 0.0

    def update(self, dt: float) -> None:
        self.current_frame += self.animation_speed * dt
        if self.current_frame > self.frames:
            self.current_frame = 0.0

    def get_frame(self) -> pygame.Surface:
        rect = pygame.Rect(int(self.current_frame) * self.width, (self.row - 1) * self.height, self.width, self.height)
        return self.texture.subsurface(rect)
