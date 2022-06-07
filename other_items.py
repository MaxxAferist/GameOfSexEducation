import pygame
from images import *


class Cell_item(pygame.sprite.Sprite):
    def __init__(self, cell, image, type):
        super().__init__()
        self.cell = cell
        self.base_image = image
        self.colid_image = lowBrightness(image, 1.8, "RGBA")
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.centerx = cell.rect.centerx
        self.rect.centery = cell.rect.centery

    def update(self, *args):
        if args:
            inv = args[0]
            if self.rect.collidepoint(pygame.mouse.get_pos()) and self.image != self.colid_image:
                self.image = self.colid_image
                if not inv.move_item:
                    inv.select_item = self
                else:
                    inv.extra_item = self
            elif not self.rect.collidepoint(pygame.mouse.get_pos()) and self.image != self.base_image:
                self.image = self.base_image
