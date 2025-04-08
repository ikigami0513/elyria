import os
import pygame
from twisted.internet import reactor
from gameserver import GameServerFactory
from world import World

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.makedirs("server/data/players", exist_ok=True)
pygame.init()
pygame.display.set_mode((1, 1))
World()

reactor.listenTCP(9000, GameServerFactory())
print("Game Server runned on port 9000...")
reactor.run()
