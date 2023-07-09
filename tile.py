import pygame
import os
import random

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'tiles')
tile_names = os.listdir(img_folder)
tile_imgs = {}
for tile_name in tile_names:
    key = tile_name.split('.')[0]
    tile_imgs[tile_name] = pygame.image.load(os.path.join(img_folder, tile_name)).convert()

class TileSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name.split('.')[0]
        self.image = tile_imgs[name]
        self.rect = self.image.get_rect()

EMPTY = 0
HORIZONTAL = 1
T_LEFT = 2
T_RIGHT = 3
CROSS = 4

class Tile:
    def __init__(self):
        self.collapsed = False
        self.options = [EMPTY, HORIZONTAL, T_LEFT, T_RIGHT, CROSS]

    def collapse(self):
        self.collapsed = True
        self.options = [random.choice(self.options)]
    
    def __repr__(self):
        return ('C' * self.collapsed + 'N' * (not self.collapsed)) + ''.join(map(str, self.options))
        