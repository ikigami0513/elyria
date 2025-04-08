import os
import pygame
from twisted.internet import reactor
from twisted.web import server
from gameserver import GameServerFactory
from dashboard.root import DashboardRoot
from world import World

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.makedirs("server/data/players", exist_ok=True)
pygame.init()
pygame.display.set_mode((1, 1))
World()

reactor.listenTCP(9000, GameServerFactory())
reactor.listenTCP(9090, server.Site(DashboardRoot()))
print("Game Server runned on port 9000...")
print("Dashboard listen on 127.0.0.1:9090")
reactor.run()
