import pygame
from images import *


class Meat(pygame.sprite.Sprite):
    image = meat
    cell_image = meat_cell
    def __init__(self, player):
        super().__init__()
        self.image = Meat.image
        self.cell_image = Meat.cell_image
        self.type = 'all'
        self.rect = self.image.get_rect()
        self.player = player

    # def update(self, *args):
    #     self.rect.x = self.player.rect.x
    #     self.rect.y = self.player.rect.y