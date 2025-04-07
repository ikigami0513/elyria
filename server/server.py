import json
from twisted.internet import protocol
from singleton import SingletonMeta
import pytmx
from pytmx.util_pygame import load_pygame


SCCALE_FACTOR = 2


class World(metaclass=SingletonMeta):
    def __init__(self):
        self.map = load_pygame("data/maps/map.tmx")

        entities_layer = self.map.get_layer_by_name("Entities")
        if entities_layer is not None and isinstance(entities_layer, pytmx.TiledObjectGroup):
            for obj in entities_layer:
                if obj.name == "PlayerSpawn":
                    self.player_spawn = (obj.x * SCCALE_FACTOR, obj.y * SCCALE_FACTOR)


class Player:
    def __init__(self, player_id, transport):
        self.id = player_id
        self.transport = transport
        self.position = World().player_spawn

    def serialize(self):
        return {
            "id": self.id,
            "position": {
                "x": self.position[0],
                "y": self.position[1]
            }
        }


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
