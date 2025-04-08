from network.abstract_handler import AbstractHandler
from typing import Dict, Any


class MoveHandler(AbstractHandler):
    def handle(self, data: Dict[Any, Any]):
        from network.gameclient import GameClient
        print(data)
        player = GameClient().players.get(data["player"])
        if not player is None and not player.is_local:
            pos_x = data["position"]["x"]
            pos_y = data["position"]["y"]
            player.pos.x = pos_x
            player.set_pos_x(pos_x)
            player.pos.y = pos_y
            player.set_pos_y(pos_y)
