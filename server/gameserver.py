import json
from twisted.internet import protocol, tcp
from singleton import SingletonMeta
from player import Player
from world import World
from handler import HANDLERS


class GameServer(protocol.Protocol, metaclass=SingletonMeta):
    next_id = 1
    transport: tcp.Server

    def __init__(self):
        self.buffer = b""

    def connectionMade(self):
        self.player_id = GameServer.next_id
        GameServer.next_id += 1

        world = World()
        player = Player.load(self.player_id, self.transport, world.player_group)
        if player is None:
            player = Player(self.player_id, self.transport, world.player_spawn, world.player_group)
            player.save()
        world.players[self.player_id] = player

        print(f"Player {self.player_id} connected.")
        self.transport.write((json.dumps({
            "action": "login",
            "player": player.serialize()
        }) + "\n").encode("utf-8"))
 
    def dataReceived(self, data):
        self.buffer += data
        while b"\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\n", 1)
            try:
                message = json.loads(line.decode())
                action = message.get("action")
                handler = HANDLERS.get(action)
                if handler:
                    handler.handle(World().players[self.player_id], message)
            except json.JSONDecodeError:
                print("Erreur JSON")

    def broadcast(self, message):
        encoded_message = (json.dumps(message) + "\n").encode("utf-8")
        for player in World().players.values():
            player.transport.write(encoded_message)

    def connectionLost(self, reason):
        world = World()
        if self.player_id in world.players:
            del world.players[self.player_id]
            print(f"Player {self.player_id} deconnected")
            self.broadcast({
                "action": "disconnect",
                "id": self.player_id
            })


class GameServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return GameServer()
