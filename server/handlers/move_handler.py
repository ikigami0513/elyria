from player import Player, Direction, State
from abstract_handler import AbstractHandler
from typing import Dict, Any


class MoveHandler(AbstractHandler):
    def handle(self, player: Player, data: Dict[str, Any]) -> None:
        from gameserver import GameServer
        player.position.x = data.get("position", {}).get("x", 0)
        player.position.y = data.get("position", {}).get("y", 0)
        GameServer().broadcast({
            "action": "move",
            "player": player.id,
            "position": {
                "x": player.position.x,
                "y": player.position.y
            }
        })
