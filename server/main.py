import os
import pygame
from twisted.internet import reactor
from server import GameServerFactory

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1, 1))

reactor.listenTCP(9000, GameServerFactory())
print("Game Server runned on port 9000...")
reactor.run()
