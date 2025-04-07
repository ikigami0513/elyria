from network.abstract_handler import AbstractHandler
from core.settings import *
from typing import Dict, Any


class LoginHandler(AbstractHandler):
    def handle(self, data: Dict[Any, Any]):
        from network.gameclient import GameClient
        from core.game import Game
        from entities.player import Player

        game = Game()
        gameclient = GameClient()
        gameclient.client_id = data["player"]["id"]
        game.world.player = Player(
            pos=(data["player"]["position"]["x"], data["player"]["position"]["y"]),
            groups=game.world.all_sprites,
            collision_sprites=game.world.collision_sprites,
            ui_layer=game.world.ui_layer,
            is_local=True,
            scale=(SCALE_FACTOR, SCALE_FACTOR)
        )
        