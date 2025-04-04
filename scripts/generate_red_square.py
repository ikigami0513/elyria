# This script is only used to generate a 16*16 pixel red square for collisions on Tiled

import pygame

pygame.init()

width, height = 16, 16

# Création de la surface
image = pygame.Surface((width, height))

image.fill((255, 0, 0))

pygame.image.save(image, "collision.png")

print("Image rouge de 16x16 créée avec succès !")
