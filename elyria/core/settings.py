DEBUG_RECT = False

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 16
SCALE_FACTOR = 3

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

TEXTURES_FILES = [
    "data/textures/player.json",
    "data/textures/layers.json",
    "data/textures/ui.json"
]

ANIMATIONS_FILES = [
    "data/animations/player.json"
]
