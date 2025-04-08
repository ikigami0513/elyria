import sys
import json
from twisted.internet import reactor, protocol, tcp
from core.settings import *
from core.singleton import SingletonMeta
from network.handler import HANDLERS
from typing import TYPE_CHECKING, Dict, Any


if TYPE_CHECKING:
    from entities.player import Player


class GameClient(protocol.Protocol, metaclass=SingletonMeta):
    transport: tcp.Client

    def __init__(self):
        self.players: Dict[int, Player] = {}
        self.client_id = None
        self.buffer = b""

    def dataReceived(self, data):
        self.buffer += data
        while b"\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\n", 1)
            try:
                message: Dict[Any, Any] = json.loads(line.decode())
                action = message.get("action")
                if not action:
                    return
                
                handler = HANDLERS.get(action)
                if not handler:
                    return
                
                handler.handle(message)
            except json.JSONDecodeError as e:
                print("Erreur JSON")
                print(e)

    def send_message(self, action: str, data=None):
        message = {"action": action}
        if data:
            message.update(data)
        self.transport.write((json.dumps(message) + "\n").encode())


class GameClientFactory(protocol.ClientFactory):
    def __init__(self):
        self.client = GameClient()

    def buildProtocol(self, addr):
        return self.client
    
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")
        from core.game import Game
        Game().running = False
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost")
        from core.game import Game
        Game().running = False
        reactor.stop()


def start_twisted():
    factory = GameClientFactory()
    reactor.connectTCP(HOST, PORT, factory)
    reactor.run(installSignalHandlers=False)
