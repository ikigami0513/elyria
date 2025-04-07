import json
import asyncio
from twisted.internet import asyncioreactor
asyncioreactor.install()

from twisted.internet import protocol
from player import Player
from tortoise import Tortoise
from models.player_model import PlayerModel


async def init_orm():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()


class GameServer(protocol.Protocol):
    players = {}
    next_id = 1

    def connectionMade(self):
        self.player_id = GameServer.next_id
        GameServer.next_id += 1

        player = Player(self.player_id, self.transport)
        GameServer.players[self.player_id] = player

        print(f"Player {self.player_id} connected.")
        self.transport.write(json.dumps({
            "action": "login",
            "player": player.serialize()
        }).encode("utf-8"))
 
    def dataReceived(self, data):
        try:
            message = json.loads(data.decode("utf-8"))
            action = message.get("action")
        except json.JSONDecodeError:
            print("Erreur de décodage JSON")

    def broadcast(self, message):
        encoded_message = json.dumps(message).encode("utf-8")
        for player in GameServer.players.values():
            player.transport.write(encoded_message)

    def connectionLost(self, reason):
        if self.player_id in GameServer.players:
            del GameServer.players[self.player_id]
            print(f"Player {self.player_id} deconnected")
            self.broadcast({
                "action": "disconnect",
                "id": self.player_id
            })


class GameServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return GameServer()
