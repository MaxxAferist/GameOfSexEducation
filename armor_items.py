import pygame
from images import *


class Spider_bib(pygame.sprite.Sprite):
    image = bib_spider
    cell_image = bib_spider_cell
    def __init__(self, player):
        super().__init__()
        self.image = Spider_bib.image
        self.cell_image = Spider_bib.cell_image
        self.type = 'bib'
        self.rect = self.image.get_rect()
        self.player = player

    def update(self, *args):
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
