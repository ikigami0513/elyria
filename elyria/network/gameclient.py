import sys
import json
from twisted.internet import reactor, protocol
from core.settings import *
from core.singleton import SingletonMeta
from network.handler import HANDLERS
from typing import TYPE_CHECKING, Dict, Any


if TYPE_CHECKING:
    from entities.player import Player


class GameClient(protocol.Protocol, metaclass=SingletonMeta):
    def __init__(self):
        self.players: Dict[int, Player] = {}
        self.client_id = None

    def dataReceived(self, data):
        message: Dict[Any, Any] = json.loads(data.decode())
        action = message.get("action")
        if not action:
            return
        
        handler = HANDLERS.get(action)
        if not handler:
            return
        
        handler.handle(message)

    def send_message(self, msg_type, data=None):
        message = {"type": msg_type}
        if data:
            message.update(data)
        self.transport.write(json.dumps(message).encode())


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
