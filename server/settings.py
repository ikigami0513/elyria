import pygame

SCALE_FACTOR = 3
TILE_SIZE = 16
PLAYER_SIZE = pygame.math.Vector2(32, 32)

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}