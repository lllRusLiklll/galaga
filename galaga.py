import os
import sys
import pygame
import time
import random

pygame.init()
pygame.display.set_mode((200, 100))
pygame.key.set_repeat(200, 70)

FPS = 30
WIDTH = 520
HEIGHT = 600
STEP = 10
LEVEL = 1

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
player_bullets = pygame.sprite.Group()


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


def load_music(name):
    fullname = os.path.join('sound', name)
    sound = pygame.mixer.Sound(fullname)
    return sound


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    start_theme.play()
    start = load_image('start.jpg')
    screen.blit(start, (0, 0))
    font = pygame.font.SysFont('Arial', 25)

    start_rendered = font.render('Start', 1, pygame.Color('green'))
    start_rect = start_rendered.get_rect()
    start_rect.top = 400
    start_rect.x = 100
    screen.blit(start_rendered, start_rect)

    quit_rendered = font.render('Quit', 1, pygame.Color('green'))
    quit_rect = quit_rendered.get_rect()
    quit_rect.top = 400
    quit_rect.x = 360
    screen.blit(quit_rendered, quit_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    start_theme.stop()
                    return
                elif quit_rect.collidepoint(event.pos):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def pause():
    end_theme.play()

    pause = load_image('pause.png')
    screen.blit(pause, (0, 0))
    font = pygame.font.SysFont('Arial', 25)

    resume_rendered = font.render('Resume', 1, pygame.Color('green'))
    resume_rect = resume_rendered.get_rect()
    resume_rect.top = 400
    resume_rect.x = 75
    screen.blit(resume_rendered, resume_rect)

    restart_rendered = font.render('Restart', 1, pygame.Color('green'))
    restart_rect = restart_rendered.get_rect()
    restart_rect.top = 400
    restart_rect.x = 230
    screen.blit(restart_rendered, restart_rect)

    quit_rendered = font.render('Quit', 1, pygame.Color('green'))
    quit_rect = quit_rendered.get_rect()
    quit_rect.top = 400
    quit_rect.x = 400
    screen.blit(quit_rendered, quit_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    end_theme.stop()
                    return True
                elif quit_rect.collidepoint(event.pos):
                    terminate()
                elif resume_rect.collidepoint(event.pos):
                    end_theme.stop()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen():
    end_theme.play()

    game_over = load_image('game_over.jpg')
    screen.blit(game_over, (0, 0))
    font = pygame.font.SysFont('Arial', 25)

    restart_rendered = font.render('Restart', 1, pygame.Color('green'))
    restart_rect = restart_rendered.get_rect()
    restart_rect.top = 400
    restart_rect.x = 100
    screen.blit(restart_rendered, restart_rect)

    quit_rendered = font.render('Quit', 1, pygame.Color('green'))
    quit_rect = quit_rendered.get_rect()
    quit_rect.top = 400
    quit_rect.x = 360
    screen.blit(quit_rendered, quit_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    end_theme.stop()
                    return True
                elif quit_rect.collidepoint(event.pos):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    end_theme.play()

    win = load_image('win.jpg')
    screen.blit(win, (0, 0))
    font = pygame.font.SysFont('Arial', 25)

    restart_rendered = font.render('Restart', 1, pygame.Color('green'))
    restart_rect = restart_rendered.get_rect()
    restart_rect.top = 400
    restart_rect.x = 100
    screen.blit(restart_rendered, restart_rect)

    quit_rendered = font.render('Quit', 1, pygame.Color('green'))
    quit_rect = quit_rendered.get_rect()
    quit_rect.top = 400
    quit_rect.x = 360
    screen.blit(quit_rendered, quit_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    end_theme.stop()
                    return True
                elif quit_rect.collidepoint(event.pos):
                    terminate()
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
        global LIFE
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
        if pygame.sprite.spritecollide(self, player_group, False):
            LIFE -= 1
            if LIFE == 0:
                pygame.sprite.spritecollide(self, player_group, True)
        if self.rect.y >= HEIGHT:
            if LIFE > 0:
                LIFE -= 1
            self.kill()

    def down(self):
        self.rect.y += 35


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
        self.add(player_bullets)
        self.image = load_image('plr_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect.y -= 7
        if pygame.sprite.spritecollide(self, aliens_group, True):
            self.kill()
            kill.play()
        if self.rect.y <= -6:
            self.kill()


class AliensBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(bullets, all_sprites)

    def update(self):
        global LIFE
        self.rect.y += 7
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


life = {1: load_image('1.png'),
        2: load_image('2.png'),
        3: load_image('3.png')}

start_theme = load_music('start.wav')
end_theme = load_music('end.wav')
kill = load_music('kill.wav')
fire = load_music('fire.wav')
level = load_music('level.wav')

while True:
    if LEVEL == 1:
        start_screen()

    level.play()
    LIFE = 3
    PAUSE = False
    BANG = 30
    DOWN = 25
    player = Player(WIDTH // 2 - 15, HEIGHT - 40)

    if LEVEL == 1:
        for i in range(0, (WIDTH // 35 - 1) * 35, 35):
            Alien3(i, 0, 3, 60)
        for i in range(10, (WIDTH // 35 - 1) * 35 + 10, 35):
            Alien2(i, 35, 2, 55)
        for i in range(5, (WIDTH // 35 - 1) * 35 + 5, 35):
            Alien1(i, 70, 1, 60)

        AMMO = 2

        pygame.time.set_timer(BANG, 1500)
        pygame.time.set_timer(DOWN, 7500)

    elif LEVEL == 2:
        for i in range(0, (WIDTH // 35 - 1) * 35, 35):
            Alien3(i, 0, 3, 60)
        for i in range(10, (WIDTH // 35 - 1) * 35 + 10, 35):
            Alien3(i, 35, 3, 55)
        for i in range(5, (WIDTH // 35 - 1) * 35 + 5, 35):
            Alien2(i, 70, 2, 55)
        for i in range(10, (WIDTH // 35 - 1) * 35 + 10, 35):
            Alien2(i, 105, 1, 55)
        for i in range(0, (WIDTH // 35 - 1) * 35, 35):
            Alien1(i, 140, 2, 60)
        for i in range(5, (WIDTH // 35 - 1) * 35 + 5, 35):
            Alien1(i, 175, 1, 60)

        AMMO = 3

        pygame.time.set_timer(BANG, 1000)
        pygame.time.set_timer(DOWN, 7000)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
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
                    if len(player_bullets.sprites()) < AMMO:
                        PlayerBullet(player.rect.x + 13, player.rect.y + 8)
                        fire.play()
                if event.key == pygame.K_ESCAPE:
                    if pause():
                        PAUSE = True
            elif event.type == BANG:
                random.choice(aliens_group.sprites()).bang()
                fire.play()
            elif event.type == DOWN:
                for i in aliens_group.sprites():
                    i.down()

        screen.blit(load_image('fon.jpg'), (0, 0))
        screen.blit(life[LIFE], (0, 250))

        aliens_group.draw(screen)
        aliens_group.update()
        player_group.draw(screen)
        bullets.draw(screen)
        bullets.update()

        pygame.display.flip()

        if len(player_group.sprites()) == 0:
            LEVEL = 1
            if game_over_screen():
                break
        if len(aliens_group.sprites()) == 0:
            if LEVEL == 1:
                LEVEL += 1
                break
            else:
                if win_screen():
                    break
        if PAUSE:
            break

        clock.tick(FPS)

    for i in all_sprites.sprites():
        i.kill()