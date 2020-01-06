import pygame
import sys
import os
from maze import maze
pygame.init()


FPS = 50
WIDTH = 650
HEIGHT = 650
maze(1, 1)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            image.set_colorkey(image.get_at((0, 0)))
    else:
        try:
            image = image.convert_alpha()
        except pygame.error:
            pass
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Лабиринт"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
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
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    screen.fill((0, 0, 0))
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('empty', x, y)
            elif level[y][x] == '.':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            pygame.display.flip()
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_screen()
player, level_x, level_y = generate_level(load_level('map.txt'))
tiles_group.draw(screen)
player_group.draw(screen)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if 50 <= player.rect.x:
                    tiles_group.draw(screen)
                    player.rect.x -= 50
                    player_group.draw(screen)
            if event.key == pygame.K_RIGHT:
                if player.rect.x <= 650:
                    tiles_group.draw(screen)
                    player.rect.x += 50
                    player_group.draw(screen)
            if event.key == pygame.K_UP:
                if 50 <= player.rect.y:
                    tiles_group.draw(screen)
                    player.rect.y -= 50
                    player_group.draw(screen)
            if event.key == pygame.K_DOWN:
                if player.rect.y <= 650:
                    tiles_group.draw(screen)
                    player.rect.y += 50
                    player_group.draw(screen)
    pygame.display.flip()
