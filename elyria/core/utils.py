import os
import sys
import pygame
from typing import Tuple


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_window_size() -> Tuple[int, int]:
    return pygame.display.get_surface().get_size()
