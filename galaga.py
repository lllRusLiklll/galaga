import os
import sys
import pygame
import time
import random

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 30
WIDTH = 520
HEIGHT = 600
STEP = 10
LIFE = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
aliens1 = pygame.sprite.Group()
aliens2 = pygame.sprite.Group()
aliens3 = pygame.sprite.Group()
bullets = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["GaLaGa", "",
                  "Правила игры",
                  "Перемещайся вправо и влево,",
                  "Стреляй в противников"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Arial', 25)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


player_image = load_image('player.png')


class Aliens(pygame.sprite.Sprite):
    def __init__(self, vx, s):
        super().__init__(aliens_group, all_sprites)
        self.vx = vx
        self.s = s
        self.ss = s
        self.wall = False
        
    def update(self):
        if self.wall:
            self.s += self.vx
            self.rect.x -= self.vx
        else:
            self.s -= self.vx
            self.rect.x += self.vx
        if self.s >= self.ss:
            self.wall = False
        elif self.s <= 0:
            self.wall = True


class Alien1(Aliens):
    def __init__(self, pos_x, pos_y, vx, s):
        super().__init__(vx, s)
        self.add(aliens1)
        self.image = load_image('alien1.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def bang(self):
        Bullet1(self.rect.x, self.rect.y + 33)
        
        
class Alien2(Aliens):
    def __init__(self, pos_x, pos_y, vx, s):
        super().__init__(vx, s)
        self.add(aliens2)
        self.image = load_image('alien2.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def bang(self):
        Bullet2(self.rect.x, self.rect.y + 33)
        
        
class Alien3(Aliens):
    def __init__(self, pos_x, pos_y, vx, s):
        super().__init__(vx, s)
        self.add(aliens3)
        self.image = load_image('alien3.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def bang(self):
        Bullet3(self.rect.x, self.rect.y + 33)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('player.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bullets, all_sprites)
        self.image = load_image('plr_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect.y -= 10
        if pygame.sprite.spritecollide(self, aliens_group, True):
            self.kill()
        if self.rect.y <= -6:
            self.kill()


class AliensBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(bullets, all_sprites)

    def update(self):
        global LIFE
        self.rect.y += 10
        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            LIFE -= 1
            if LIFE == 0:
                pygame.sprite.spritecollide(self, player_group, True)
        if self.rect.y >= HEIGHT + 6:
            self.kill()


class Bullet1(AliensBullet):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('bullet1.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Bullet2(AliensBullet):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('bullet2.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Bullet3(AliensBullet):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('bullet3.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


start_screen()

player = Player(WIDTH // 2 - 15, HEIGHT - 40)

for i in range(0, WIDTH // 35 * 35, 35):
    Alien3(i, 0, 3, 30)
for i in range(10, WIDTH // 35 * 35 + 10, 35):
    Alien2(i, 35, 2, 25)
for i in range(5, WIDTH // 35 * 35 + 5, 35):
    Alien1(i, 70, 1, 30)

running = True
BANG = 30
pygame.time.set_timer(BANG, 1800)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= STEP
                if player.rect.x <= -30:
                    player.rect.x = WIDTH - STEP
            if event.key == pygame.K_RIGHT:
                player.rect.x += STEP
                if player.rect.x >= WIDTH:
                    player.rect.x = STEP - 30
            if event.key == pygame.K_SPACE:
                PlayerBullet(player.rect.x + 13, player.rect.y + 8)
        elif event.type == BANG:
            random.choice(aliens_group.sprites()).bang()

    screen.fill(pygame.Color(0, 0, 0))

    aliens_group.draw(screen)
    aliens_group.update()
    player_group.draw(screen)
    bullets.draw(screen)
    bullets.update()

    pygame.display.flip()

    clock.tick(FPS)

terminate()
