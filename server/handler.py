from abstract_handler import AbstractHandler
from handlers.move_handler import MoveHandler
from typing import Dict


HANDLERS: Dict[str, AbstractHandler] = {
    "move": MoveHandler()
}