from player import Player
from abc import ABC
from typing import Dict, Any


class AbstractHandler(ABC):
    def handle(self, player: Player, data: Dict[str, Any]) -> None:
        pass
