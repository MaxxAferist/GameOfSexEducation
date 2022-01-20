import pygame
import sys
import os
from ctypes import *


pygame.init()
pygame.mixer.init()
FPS = 60
WIDTH = windll.user32.GetSystemMetrics(0)
HEIGHT = windll.user32.GetSystemMetrics(1)
SOUNDS = [pygame.mixer.Sound('data//sounds//Steps.mp3')]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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
        while self.running:
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
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        image = load_image('game_fon.png')
        self.fon.image = image
        self.fon.rect = image.get_rect()
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data//music//game_music.mp3')
        pygame.mixer.music.set_volume(0.04)
        pygame.mixer.music.play()
        self.running = True

    def run(self):
        rock = Wall((100, 200), 'rock')
        self.all_sprites.add(rock)
        player = Player((1000, 400))
        self.player_sprite = pygame.sprite.Group()
        self.player_sprite.add(player)
        for phrase in player.phrases:
            phrase.add_groups()
        self.walls_sprites.add(rock)
        camera = Camera()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    go_menu()
            camera.update(player, self.fon)
            for sprite in self.all_sprites:
                camera.apply(sprite)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.player_sprite.update(self.walls_sprites)
            self.player_sprite.draw(self.screen)
            pygame.display.flip()
            self.screen.fill(pygame.Color(0, 0, 0))
            self.clock.tick(FPS)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.image = pygame.transform.scale(load_image(f'objects//{type}.png'), (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image_1 = pygame.transform.scale(load_image('creature//player.png'), (100, 100))
        self.image_2 = pygame.transform.scale(load_image('creature//player_run_1.png'), (100, 100))
        self.image_2_flip = pygame.transform.flip(self.image_2, True, False)
        self.image_3 = pygame.transform.scale(load_image('creature//player_run_2.png'), (100, 100))
        self.image_3_flip = pygame.transform.flip(self.image_3, True, False)
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.v = 4
        self.n_animation = 0
        self.n_animation_limit = 10
        self.phrases = [Messege('Соблюдай дистанцию', self, 30)]

    def check_colide(self, walls, type_move):
        stack_sprite = pygame.sprite.Sprite()
        stack_sprite.rect = self.rect.copy()
        if type_move == 'right':
            stack_sprite.rect.x += self.v
        if type_move == 'left':
            stack_sprite.rect.x -= self.v
        if type_move == 'down':
            stack_sprite.rect.y += self.v
        if type_move == 'up':
            stack_sprite.rect.y -= self.v
        for wall in walls:
            if pygame.sprite.collide_rect(stack_sprite, wall):
                return False
        return True

    def update(self, walls):
        keys = pygame.key.get_pressed()
        if any([keys[pygame.K_d], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_w]]):
            animate_flag = False
            if keys[pygame.K_d]:
                if self.check_colide(walls, 'right'):
                    animate_flag = True
                    if self.rect.x + self.rect.w + self.v <= WIDTH:
                        self.rect.x += self.v
                    else:
                        animate_flag = False
                        self.rect.x = WIDTH - self.rect.w
            if keys[pygame.K_a]:
                if self.check_colide(walls, 'left'):
                    animate_flag = True
                    if self.rect.x - self.v >= 0:
                        self.rect.x -= self.v
                    else:
                        animate_flag = False
                        self.rect.x = 0
            if keys[pygame.K_w]:
                if self.check_colide(walls, 'up'):
                    animate_flag = True
                    if self.rect.y - self.v >= 0:
                        self.rect.y -= self.v
                    else:
                        animate_flag = False
                        self.rect.y = 0
            if keys[pygame.K_s]:
                if self.check_colide(walls, 'down'):
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


            if SOUNDS[0].get_num_channels() == 0:
                SOUNDS[0].play()
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


class Camera():
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, other):
        other.rect.x += self.dx
        other.rect.y += self.dy

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
        self.rect.w = len(text) * (font_size + 10)
        self.rect.h = font_size + 10
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
        self.up_top = (self.rect.h - self.font_size) // 2
        self.left_top = (self.rect.w - self.text.get_rect()[2]) // 2
        self.image.blit(self.text, (self.left_top, self.up_top))
        self.player = player

    def update(self):
        self.rect.x = self.player.rect.x + 0.75 * self.player.rect.w
        self.rect.y = self.player.rect.y + self.rect.h + 5

    def add_groups(self):
        for group in self.player.groups():
            group.add(self)


if __name__ == '__main__':
    go_menu()
