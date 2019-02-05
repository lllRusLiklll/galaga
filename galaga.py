import os
import sys
import pygame
import time

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 520
HEIGHT = 700
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()


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


'''def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках            
    return new_player, x, y'''


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


aliens = {'alien1': load_image('alien1.png'), 
          'alien2': load_image('alien2.png'), 
          'alien3': load_image('alien3.png')}
player_image = load_image('player.png')


class Aliens(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(aliens_group, all_sprites)
        self.wall = False
        self.vx = 1
        self.s = 30
        
    def update(self):
        if not self.wall:
            if self.rect.x + self.rect[2] == WIDTH:
                self.wall = True
            else:
                self.rect.x += self.vx
        else:
            if self.rect.x == 0:
                self.wall = False 
            else:
                self.rect.x -= self.vx


class Alien1(Aliens):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('alien1.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        
class Alien2(Aliens):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('alien2.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        
class Alien3(Aliens):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('alien3.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('player.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


start_screen()

player = Player(WIDTH // 2 - 15, HEIGHT - 40)

for i in range(0, WIDTH // 35 * 35, 35):
    Alien1(i, 0)
for i in range(WIDTH - WIDTH // 35 * 35, WIDTH, 35):
    Alien2(i, 35)
for i in range(WIDTH - WIDTH // 35 * 35 - 17, WIDTH - 17, 35):
    Alien3(i, 70)

running = True

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

    screen.fill(pygame.Color(0, 0, 0))
    aliens_group.draw(screen)
    aliens_group.update()
    player_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

terminate()
