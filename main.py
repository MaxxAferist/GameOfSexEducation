import pygame
import sys
import os
from ctypes import *
from PIL import Image, ImageEnhance
import numpy as np
import os
from food_items import *
from armor_items import *
from weapon_items import *
from other_items import *
from images import *


pygame.init()
pygame.mixer.init()
FPS = 60
WIDTH = windll.user32.GetSystemMetrics(0)
HEIGHT = windll.user32.GetSystemMetrics(1)
SOUNDS = [pygame.mixer.Sound('data//sounds//Steps.mp3')]


def termit():
    sys.exit()


def go_game():
    game = Game()
    game.run()


def go_menu():
    menu = Menu()
    menu.run()


class Menu():
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        fon_image = load_image('Vasya_noop.png')
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        self.fon.image = fon_image
        self.fon.rect = self.fon.image.get_rect()
        self.running = True
        self.buttons_sprites = pygame.sprite.Group()
        buttons = ['New game', 'Load game', 'Settings', 'Exit']
        actions = [go_game, None, None, termit]
        btn_w = 300
        btn_h = 60
        top = 10
        font_size = 30
        left_top = (WIDTH - btn_w) // 2
        up_top = (HEIGHT - btn_h * len(buttons) - top * (len(buttons) - 1)) // 2
        for i in range(len(buttons)):
            button = Button(buttons[i], (left_top, up_top + (btn_h + top) * i, btn_w, btn_h), font_size, actions[i])
            self.buttons_sprites.add(button)
            self.all_sprites.add(button)

    def run(self):
        pygame.mixer.music.load('data//music//O.G.Troiboy.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0)
        while self.running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    termit()
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)


class Button(pygame.sprite.Sprite):
    def __init__(self, name, rect, font_size, action=None):
        super().__init__()
        image = pygame.Surface(rect[2:])
        image.fill(pygame.Color(200, 200, 200))
        self.fon = image
        self.image = self.fon
        self.rect = image.get_rect()
        self.rect.x = rect[0]
        self.rect.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.font_size = font_size
        f = pygame.font.Font(None, self.font_size)
        self.name = name
        self.text = f.render(self.name, True, (0, 0, 0))
        self.up_top = (self.h - self.font_size) // 2
        self.left_top = (self.w - self.text.get_rect()[2]) // 2
        self.image.blit(self.text, (self.left_top, self.up_top))
        self.click_flag = False
        self.pressed = False
        self.action = action

    def update(self):
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(pos) and pressed:
            f = pygame.font.Font(None, self.font_size)
            self.image = self.fon
            self.text = f.render(self.name, True, (255, 255, 0))
            self.image.blit(self.text, (self.left_top, self.up_top))
            self.pressed = True
        elif self.rect.collidepoint(pos) and self.pressed and not pressed:
            self.pressed = False
            if self.click_flag and self.action:
                self.action()
        elif self.rect.collidepoint(pos):
            self.click_flag = True
            f = pygame.font.Font(None, self.font_size)
            self.image = self.fon
            self.text = f.render(self.name, True, (0, 162, 232))
            self.image.blit(self.text, (self.left_top, self.up_top))
        else:
            self.pressed = False
            f = pygame.font.Font(None, self.font_size)
            self.image = self.fon
            self.text = f.render(self.name, True, (0, 0, 0))
            self.image.blit(self.text, (self.left_top, self.up_top))


class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.walls_sprites = pygame.sprite.Group()
        self.nps_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        image = load_image('game_fon.png')
        self.fon.image = image
        self.fon.rect = image.get_rect()
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data//music//game_music.mp3')
        #pygame.mixer.music.set_volume(0.04)
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play()
        self.running = True

    def run(self):
        self.add_sprites()
        camera = Camera()
        while self.running:
            self.reset_images()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    go_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.inventory.run(self)
            camera.update(self.player, self.fon)
            for sprite in self.all_sprites:
                camera.apply(sprite)
            for sprite in self.nps_sprites:
                if type(sprite) in self.nps_types:
                    camera.apply_for_nps(sprite)
            self.player.update(self.walls_sprites)
            self.knight.update(self.walls_sprites)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.screen.fill(pygame.Color(0, 0, 0))
            self.clock.tick(FPS)

    def reset_images(self):
        for wall in self.walls_sprites:
            wall.norm_Brighntess()

    def add_sprites(self):
        self.nps_types = [Knight]
        rock = Wall((100, 200), 'rock', 10)
        self.all_sprites.add(rock)
        self.player = Player((1000, 400))
        self.knight = Knight((500, 300), self.fon, self.player, self)
        self.all_sprites.add(self.knight)
        self.nps_sprites.add(self.knight)
        for phrase in self.knight.phrases:
            phrase.add_groups()
        self.all_sprites.add(self.player)
        for phrase in self.player.phrases:
            phrase.add_groups()
        self.player.ray.add_groups()
        self.walls_sprites.add(rock)
        self.inventory = Inventory(self.player.inventory)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, type, k):
        super().__init__()
        image = load_image(f'objects//{type}.png')
        self.image = pygame.transform.scale(image, (image.get_width() * k, image.get_height() * k))
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def low_Brightness(self):
        self.image = self.base_image.copy()
        self.image = lowBrightness(self.image, 0.5, "RGBA")

    def norm_Brighntess(self):
        self.image = self.base_image.copy()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image_1 = pygame.transform.scale(load_image('creature//player.png'), (80, 140))
        self.image_2 = pygame.transform.scale(load_image('creature//player_run_1.png'), (80, 140))
        self.image_2_flip = pygame.transform.flip(self.image_2, True, False)
        self.image_3 = pygame.transform.scale(load_image('creature//player_run_2.png'), (80, 140))
        self.image_3_flip = pygame.transform.flip(self.image_3, True, False)
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.v = 4
        self.n_animation = 0
        self.n_animation_limit = 10
        self.phrases = [Messege('ДА БЛЯТЬ ЛОБ БОЛИТ', self, 30)]
        self.ray = Ray(self, 300, 10, [139, 0, 0])
        self.mask = pygame.mask.from_surface(self.image)
        self.inventory = [[0] * 6] + [[0] * 6] * 4 + [[0] * 4] + [[0] * 3]
        self.inventory[0][0] = Spider_bib(self)
        self.inventory[5][0] = Meat(self)

    def check_colide_move(self, walls, type_move):
        stack_sprite = pygame.sprite.Sprite()
        stack_sprite.rect = self.rect.copy()
        stack_sprite.mask = pygame.mask.from_surface(pygame.Surface((self.rect.w, self.rect.h)))
        if type_move == 'right':
            stack_sprite.rect.x += self.v
        if type_move == 'left':
            stack_sprite.rect.x -= self.v
        if type_move == 'down':
            stack_sprite.rect.y += self.v
        if type_move == 'up':
            stack_sprite.rect.y -= self.v
        for wall in walls:
            if pygame.sprite.collide_mask(stack_sprite, wall):
                return False
        return True

    def update(self, *args):
        if args:
            walls = args[0]
            keys = pygame.key.get_pressed()
            self.phrases[0].show = False
            if pygame.mouse.get_pressed()[0]:
                self.ray.update(True)
                for wall in walls:
                    if pygame.sprite.collide_mask(self.ray, wall):
                        wall.low_Brightness()
            else:
                self.ray.update(False)
            if any([keys[pygame.K_d], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_w]]):
                animate_flag = False
                if keys[pygame.K_d]:
                    if self.check_colide_move(walls, 'right'):
                        animate_flag = True
                        if self.rect.x + self.rect.w + self.v <= WIDTH:
                            self.rect.x += self.v
                        else:
                            animate_flag = False
                            self.rect.x = WIDTH - self.rect.w
                if keys[pygame.K_a]:
                    if self.check_colide_move(walls, 'left'):
                        animate_flag = True
                        if self.rect.x - self.v >= 0:
                            self.rect.x -= self.v
                        else:
                            animate_flag = False
                            self.rect.x = 0
                if keys[pygame.K_w]:
                    if self.check_colide_move(walls, 'up'):
                        animate_flag = True
                        if self.rect.y - self.v >= 0:
                            self.rect.y -= self.v
                        else:
                            animate_flag = False
                            self.rect.y = 0
                if keys[pygame.K_s]:
                    if self.check_colide_move(walls, 'down'):
                        animate_flag = True
                        if self.rect.y + self.rect.h + self.v <= HEIGHT:
                            self.rect.y += self.v
                        else:
                            animate_flag = False
                            self.rect.y = HEIGHT - self.rect.h
                if animate_flag:
                    self.change_image()
                else:
                    self.image = self.image_1
                    self.phrases[0].show = True

                # if SOUNDS[0].get_num_channels() == 0:
                #     SOUNDS[0].play()
            else:
                self.image = self.image_1

    def change_image(self):
        if self.n_animation == self.n_animation_limit:
            if self.image == self.image_1:
                self.image = self.image_2
            elif self.image == self.image_2:
                self.image = self.image_3
            elif self.image == self.image_3:
                self.image = self.image_2
            self.n_animation = 0
        else:
            self.n_animation += 1
        self.mask = pygame.mask.from_surface(self.image)


class Knight(pygame.sprite.Sprite):
    def __init__(self, pos, fon, player, table):
        super().__init__()
        self.image_1 = pygame.transform.scale(load_image('creature//knight.png'), (110, 140))
        self.image_2 = pygame.transform.scale(load_image('creature//knight_run_1.png'), (110, 140))
        self.image_2_flip = pygame.transform.flip(self.image_2, True, False)
        self.image_3 = pygame.transform.scale(load_image('creature//knight_run_2.png'), (110, 140))
        self.image_3_flip = pygame.transform.flip(self.image_3, True, False)
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.fon = fon
        self.rect.x = self.fon.rect.x + pos[0]
        self.rect.y = self.fon.rect.y + pos[1]
        self.v = 1
        self.n_animation = 0
        self.n_animation_limit = 10
        self.phrases = [Messege('ЬЛЯТЬ ОТВАЛИ', self, 30)]
        self.mask = pygame.mask.from_surface(self.image)
        self.k_pos = [self.rect.x, self.rect.y]
        self.player = player
        self.table = table

    def check_colide_move(self, walls, type_move):
        stack_sprite = pygame.sprite.Sprite()
        stack_sprite.rect = self.rect.copy()
        stack_sprite.mask = self.mask.copy()
        if type_move == 'right':
            stack_sprite.rect.x += self.v
        if type_move == 'left':
            stack_sprite.rect.x -= self.v
        if type_move == 'down':
            stack_sprite.rect.y += self.v
        if type_move == 'up':
            stack_sprite.rect.y -= self.v
        for wall in walls:
            if pygame.sprite.collide_mask(stack_sprite, wall):
                return False
        return True

    def range_from_player(self, r):
        if ((self.rect.centerx - self.player.rect.centerx) ** 2 + (self.rect.centery - self.player.rect.centery) ** 2) ** 0.5 <= r:
            return True
        return False

    def update(self, *args):
        if args:
            walls = args[0]
            self.phrases[0].show = False
            if self.k_pos != [self.rect.x, self.rect.y]:
                self.go_walk(self.k_pos)
                self.change_image()
            else:
                self.image = self.image_1
            if self.range_from_player(150):
                key = pygame.key.get_pressed()[pygame.K_e]
                if key:
                    dialog = dialogWindow('Ты еблан?')
                    dialog.run(self.table)

    def go_walk(self, pos):
        self.k = (pos[1] - self.rect.y) / (pos[0] - self.rect.x)
        self.b = self.rect.y - (self.k * self.rect.x)
        if pos[0] > self.rect.x:
            self.rect.x += self.v
        else:
            self.rect.x -= self.v
        self.rect.y = self.k * self.rect.x + self.b

    def go_coords(self, pos, fon=True):
        if fon:
            self.k_pos = [self.fon.rect.x + pos[0], self.fon.rect.y + pos[1]]
        else:
            self.k_pos = pos

    def change_image(self):
        if self.n_animation == self.n_animation_limit:
            if self.image == self.image_1:
                self.image = self.image_2
            elif self.image == self.image_2:
                self.image = self.image_3
            elif self.image == self.image_3:
                self.image = self.image_2
            self.n_animation = 0
        else:
            self.n_animation += 1
        self.mask = pygame.mask.from_surface(self.image)


class dialogWindow():
    def __init__(self, text):
        self.phrase = text
        self.answers = [['Что нахуй происходит?', self.stop],
                        ['Блять ты кто', self.stop],
                        ['Ахуеть', self.stop],
                        ['Ну сколько можно...', self.stop],
                        ['Засунь се в жопу огурец', self.stop]]
        self.index_select = 0
        self.all_sprites = pygame.sprite.Group()

    def add_answer(self, answer):
        self.answers.append(answer)

    def stop(self):
        self.running = False

    def add_sprites(self, other):
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        image = lowBrightness(other.screen.subsurface(pygame.Rect(0, 0, WIDTH, HEIGHT)), 0.5, "RGB")
        self.fon.image = image
        self.fon.rect = self.fon.image.get_rect()
        self.dialog_window = pygame.sprite.Sprite(self.all_sprites)
        self.dialog_window.image = load_image('dialog.png')
        self.dialog_window.rect = self.dialog_window.image.get_rect()
        self.dialog_window.rect.x = (WIDTH - self.dialog_window.rect.w) // 2
        self.dialog_window.rect.y = HEIGHT - self.dialog_window.rect.h

        self.answers_sprites = pygame.sprite.Group()
        for i in range(len(self.answers)):
            answer = Answer(self.answers[i][0], self.answers[i][1],
                            (self.dialog_window.rect.x + 10, self.dialog_window.rect.y + 50 + i * 27),
                            (self.dialog_window.rect.w, 40))
            self.answers_sprites.add(answer)
        self.answers_sprites.sprites()[self.index_select].select = True
        self.answers_sprites.sprites()[self.index_select].change_select()
        self.all_sprites.add(self.answers_sprites)

    def run(self, other):
        other.all_sprites.draw(other.screen)
        pygame.display.flip()
        self.add_sprites(other)
        self.running = True
        while self.running:
            other.screen.fill(pygame.Color(0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.answers_sprites.sprites()[self.index_select].select = False
                        self.answers_sprites.sprites()[self.index_select].change_select()
                        if self.index_select == 0:
                            self.index_select = len(self.answers_sprites)
                        self.index_select -= 1
                    if event.key == pygame.K_DOWN:
                        self.answers_sprites.sprites()[self.index_select].select = False
                        self.answers_sprites.sprites()[self.index_select].change_select()
                        if self.index_select == len(self.answers_sprites) - 1:
                            self.index_select = -1
                        self.index_select += 1
                    self.answers_sprites.sprites()[self.index_select].select = True
                    self.answers_sprites.sprites()[self.index_select].change_select()
                    if event.key == pygame.K_RETURN:
                        self.answers_sprites.sprites()[self.index_select].action()
            self.all_sprites.update()
            self.all_sprites.draw(other.screen)
            pygame.display.flip()
            other.clock.tick(FPS)


class Answer(pygame.sprite.Sprite):
    def __init__(self, text, action, pos, size):
        super().__init__()
        self.w, self.h = size
        self.answer = text
        self.select = False
        self.font = pygame.font.Font(os.path.join(os.getcwd(), 'data', '18965.ttf'), 15)
        self.change_select()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.action = action

    def change_select(self):
        if self.select:
            self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            self.text = self.font.render(self.answer, True, (247, 242, 26))
            self.image.blit(self.text, (0, 0))
        else:
            self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            self.text = self.font.render(self.answer, True, (0, 110, 189))
            self.image.blit(self.text, (0, 0))


class Camera():
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, other):
        other.rect.x += self.dx
        other.rect.y += self.dy

    def apply_for_nps(self, nps):
        nps.k_pos[0] += self.dx
        nps.k_pos[1] += self.dy

    def update(self, target, fon):
        self.dx = (WIDTH - target.rect.w) // 2 - target.rect.x
        self.dy = (HEIGHT - target.rect.h) // 2 - target.rect.y
        if not (fon.rect.x + self.dx <= 0 and fon.rect.x + fon.rect.w + self.dx >= WIDTH):
            self.dx = 0
        if not (fon.rect.y + self.dy <= 0 and fon.rect.y + fon.rect.h + self.dy >= HEIGHT):
            self.dy = 0


class Messege(pygame.sprite.Sprite):
    def __init__(self, text, player, font_size):
        super().__init__()
        self.rect = pygame.Surface((0, 0)).get_rect()
        self.rect.w = len(text) * font_size // 2
        self.rect.h = font_size
        self.rect.x = player.rect.x + 0.75 * player.rect.w
        self.rect.y = player.rect.y + self.rect.h + 5
        image = pygame.Surface((self.rect.w, self.rect.h))
        image.fill(pygame.Color(200, 200, 200))
        self.fon = image
        self.image = self.fon
        self.rect = image.get_rect()
        self.font_size = font_size
        f = pygame.font.Font(None, self.font_size)
        self.name = text
        self.text = f.render(self.name, True, (0, 0, 0))
        self.up_top = (self.rect.h - self.text.get_rect()[3]) // 2
        self.left_top = (self.rect.w - self.text.get_rect()[2]) // 2
        self.image.blit(self.text, (self.left_top, self.up_top))
        self.player = player
        self.show = False

    def update(self):
        if self.show:
            self.rect.x = self.player.rect.x + 0.75 * self.player.rect.w
            self.rect.y = self.player.rect.y - self.rect.h - 5
        else:
            self.rect.x = -1000
            self.rect.y = -1000

    def add_groups(self):
        for group in self.player.groups():
            group.add(self)


class Ray(pygame.sprite.Sprite):
    def __init__(self, player, distance, tal, color):
        super().__init__()
        self.rect = pygame.Surface((0, 0)).get_rect()
        self.distance = distance
        self.tal = tal
        self.player = player
        self.image = pygame.Surface((0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        image = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.image = image
        self.color = color + [170]

    def update(self, *args):
        if args:
            if args[0]:
                player_pos = (self.player.rect.centerx, self.player.rect.centery)
                pos = pygame.mouse.get_pos()
                try:
                    k = (pos[1] - player_pos[1]) / (pos[0] - player_pos[0])
                    if pos[0] > player_pos[0] and pos[1] <= player_pos[1]:
                        alpha = np.arctan(-k) * 180 / np.pi
                    elif pos[0] <= player_pos[0] and pos[1] <= player_pos[1]:
                        alpha = 180 + np.arctan(-k) * 180 / np.pi
                    elif pos[0] <= player_pos[0] and pos[1] > player_pos[1]:
                        alpha = 180 + np.arctan(-k) * 180 / np.pi
                    else:
                        alpha = 360 + np.arctan(-k) * 180 / np.pi
                    alpha = np.radians(alpha)

                    x_p = np.cos(np.radians(90 - np.degrees(alpha))) * self.tal
                    y_p = np.sin(np.radians(90 - np.degrees(alpha))) * self.tal

                    X = np.cos(alpha) * self.distance
                    Y = np.sin(alpha) * self.distance

                    w = max(abs(-x_p + X), abs(x_p + X)) * 2
                    h = max(abs(-y_p - Y), abs(y_p - Y)) * 2

                    image = pygame.Surface((w, h), pygame.SRCALPHA)

                    x = image.get_width() // 2
                    y = image.get_height() // 2

                    pygame.draw.polygon(image, self.color, ((x - x_p, y - y_p),
                                                             (x - x_p + X, y - y_p - Y),
                                                             (x + x_p + X, y + y_p - Y),
                                                             (x + x_p, y + y_p)))
                    pygame.draw.circle(image, self.color, (x, y), self.tal)
                    self.image = image.copy()

                    self.rect = self.image.get_rect()
                    self.rect.centerx = self.player.rect.centerx
                    self.rect.centery = self.player.rect.centery
                    self.mask = pygame.mask.from_surface(self.image)
                except:
                    pass
            else:
                self.rect.x = -10000
                self.rect.y = -10000

    def add_groups(self):
        for group in self.player.groups():
            group.add(self)


class Inventory():
    def __init__(self, invent):
        self.all_sprites = pygame.sprite.Group()
        self.statik_sprite = pygame.sprite.Group()
        self.font = pygame.font.Font(os.path.join(os.getcwd(), 'data', '19718.ttf'), 15)
        self.cell_size = [65, 65]
        self.invent = invent
        self.items = [[0] * 6] + [[0] * 6] * 4 + [[0] * 4] + [[0] * 3]

    def add_sprites(self, other):
        self.fon = pygame.sprite.Sprite(self.statik_sprite)
        image = lowBrightness(other.screen, 0.5, "RGB")
        self.fon.image = image
        self.fon.rect = self.fon.image.get_rect()
        self.inventory_window = pygame.sprite.Sprite(self.statik_sprite)
        self.inventory_window.image = load_image('fon_inventary6.png')
        self.inventory_window.rect = self.inventory_window.image.get_rect()
        self.inventory_window.rect.x = (WIDTH - self.inventory_window.rect.w) // 2
        self.inventory_window.rect.y = (HEIGHT - self.inventory_window.rect.h) // 2

        promezh = 4
        self.cells = []
        left_top = self.inventory_window.rect.x + 340
        up_top = self.inventory_window.rect.y + 361
        cells_sprites = pygame.sprite.Group()
        for i in range(6):
            cell = Inventory_cell('all')
            cell.rect.x = left_top + i * (cell.rect.w + promezh)
            cell.rect.y = up_top
            cells_sprites.add(cell)
        self.cells.append(cells_sprites)

        left_top = self.inventory_window.rect.x + 30
        up_top = self.inventory_window.rect.y + 25
        for i in range(4):
            cells_sprites = pygame.sprite.Group()
            for j in range(6):
                cell = Inventory_cell('all')
                cell.rect.x = left_top + i * (cell.rect.w + promezh)
                cell.rect.y = up_top + j * (cell.rect.h + promezh)
                cells_sprites.add(cell)
            self.cells.append(cells_sprites)

        self.description_border = pygame.sprite.Sprite()
        self.description_base_image = pygame.transform.scale(load_image('description_of_items2.png'), (250, 250))
        self.description_border.image = self.description_base_image.copy()
        self.description_border.rect = self.description_border.image.get_rect()
        self.description_border.rect.x = self.inventory_window.rect.x + 340
        self.description_border.rect.y = up_top
        self.statik_sprite.add(self.description_border)
        self.change_description('Василий не дрочи')

        left_top = self.inventory_window.rect.x + 650
        armor_types = ['helmet', 'bib', 'pens', 'bots']
        cells_sprites = pygame.sprite.Group()
        for i in range(4):
            cell = Inventory_cell(armor_types[i])
            cell.rect.x = left_top
            cell.rect.y = up_top + i * (cell.rect.h + promezh)
            cells_sprites.add(cell)
        self.cells.append(cells_sprites)

        self.player_base_image = pygame.transform.scale(load_image('creature/player.png'), (160, 280))
        self.hanger = pygame.sprite.Sprite()
        self.hanger.image = self.player_base_image.copy()
        self.hanger.rect = self.hanger.image.get_rect()
        self.hanger.rect.x = self.inventory_window.rect.x + 775
        self.hanger.rect.y = up_top
        self.all_sprites.add(self.hanger)

        cells_sprites = pygame.sprite.Group()
        left_top = self.inventory_window.rect.w + self.inventory_window.rect.x - (self.cell_size[0] + 30)
        for i in range(3):
            if i <= 1:
                cell = Inventory_cell('ring')
            else:
                cell = Inventory_cell('amulet')
            cell.rect.x = left_top
            cell.rect.y = up_top + i * (cell.rect.h + promezh)
            cells_sprites.add(cell)
        self.cells.append(cells_sprites)
        for group in self.cells:
            self.all_sprites.add(group)

    def change_description(self, text):
        text = self.font.render(text, True, (0, 33, 55))
        image = self.description_base_image.copy()
        image.blit(text, (20, 10))
        self.description_border.image = image

    def init_inventoty(self):
        for i in range(len(self.invent)):
            for j in range(len(self.invent[i])):
                if self.invent[i][j] != 0:
                    cell = self.cells[i].sprites()[j]
                    image = self.invent[i][j].cell_image
                    type = self.invent[i][j].type
                    self.items[i][j] = Cell_item(cell, image, type)
        for i in range(len(self.items)):
            for elem in self.items[i]:
                if elem != 0:
                    self.all_sprites.add(elem)

    def run(self, other):
        other.all_sprites.draw(other.screen)
        pygame.display.flip()
        self.add_sprites(other)
        self.init_inventoty()
        self.running = True
        while self.running:
            other.screen.fill(pygame.Color(0, 0, 0))
            self.select_item = None
            self.extra_item = None
            self.all_sprites.update(self)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                # if 
            self.statik_sprite.draw(other.screen)
            self.all_sprites.draw(other.screen)
            pygame.display.flip()
            other.clock.tick(FPS)


class Inventory_cell(pygame.sprite.Sprite):
    image = lowBrightness(load_image('cell.png'), 1.5, "RGB")
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.base_image = Inventory_cell.image
        self.colid_image = lowBrightness(self.base_image.copy(), 1.8, "RGB")
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

    def update(self, *args):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.image != self.colid_image:
            self.image = self.colid_image
        elif not self.rect.collidepoint(pygame.mouse.get_pos()) and self.image != self.base_image:
            self.image = self.base_image


if __name__ == '__main__':
    go_menu()
