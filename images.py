import os
import sys
import pygame
from PIL import Image, ImageEnhance

def pilToSurface(pilImage):
    return pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode)


def surfaceToPil(surface, format):
    pil_string_image = pygame.image.tostring(surface, format, False)
    return Image.frombuffer(format, surface.get_size(), pil_string_image)


def lowBrightness(image, factor, format):
    pil_image = surfaceToPil(image, format)
    enhancer = ImageEnhance.Brightness(pil_image)
    image_final = enhancer.enhance(factor)
    return pilToSurface(image_final)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


bib_spider = load_image('items/Armors/bib_spider.png')
bib_spider_cell = load_image('items/Armors_items/bib_spider.png')
meat = load_image('items/Food/meat.png')
meat_cell = load_image('items/Food_items/meat.png')
