import pygame
import sys
import os
from maze import maze
import random
from datetime import datetime

pygame.init()

GRAVITY = -0.008
width = 650
height = 650
screen_rect = (0, 0, width, height)
all_sprites = pygame.sprite.Group()


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


particles_group = pygame.sprite.Group()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Particle(pygame.sprite.Sprite):
    fire = [load_image("ball.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites, particles_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def end_screen(length):
    size = width, height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Maze')
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    running = True
    show_time(length)
    while running:
        show_time(length)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
        screen.blit(fon, (0, 0))
        clock.tick(50)
        show_time(duration)
        particles_group.update()
        particles_group.draw(screen)
        pygame.display.flip()


def show_time(difference):
    seconds = difference % 60
    mins = str((difference - seconds) // 60)
    seconds = str(seconds)
    text = "Время: {} минут, {} секунд".format(mins, seconds)
    pygame.display.set_caption('Maze')
    text_coord = 60
    font = pygame.font.Font("data/font.ttf", 27)
    string_rendered = font.render(text, 1, (92, 30, 50))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 120
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)


FPS = 50
WIDTH = 650
HEIGHT = 650
balls = 0


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def rules():
    pygame.display.set_caption('Rules')
    fon = pygame.transform.scale(load_image('start.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    intro_text = ["\nПравила\n",
                  "",
                  "Что бы пройти игру, нужно",
                  "собрать все мячики,",
                  "пройти все уровни.",
                  "У Вас нет возможности",
                  "наступать на препятствия.",
                  "",
                  "Уровень считается пройденным, ",
                  "если вы собрали все мячики.",
                  ""]
    text_coord = 100
    for line in intro_text:
        font = pygame.font.Font("data/font.ttf", 25)
        string_rendered = font.render(line, 1, (92, 30, 50))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font("data/font.ttf", 35)
    text = font.render("Назад", 1, (102, 0, 102))
    text_x = 20
    text_y = 570
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (163, 88, 232), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20), 5)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 20 <= x <= 158 and 570 <= y <= 606:
                    screen.blit(fon, (0, 0))
                    return
        pygame.display.flip()
        clock.tick(FPS)


def info():
    pygame.display.set_caption('Info')
    fon = pygame.transform.scale(load_image('start.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    intro_text = ["\nОб Игре\n",
                  "",
                  "Игра в жанре 'Лабиринт'",
                  "",
                  "Автор: Чурина Маргарита",
                  "",
                  "email:",
                  "elshanskaya.r@inbox.ru",
                  "",
                  "Яндекс почта:",
                  "tchurina.margaery@yandex.ru",
                  ""]
    text_coord = 100
    for line in intro_text:
        font = pygame.font.Font("data/font.ttf", 25)
        string_rendered = font.render(line, 1, (92, 30, 50))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font("data/font.ttf", 35)
    text = font.render("Назад", 1, (102, 0, 102))
    text_x = 20
    text_y = 570
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (163, 88, 232), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20), 5)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 20 <= x <= 158 and 570 <= y <= 606:
                    screen.blit(fon, (0, 0))
                    return
        pygame.display.flip()
        clock.tick(FPS)


def draw_buttons():
    font = pygame.font.Font("data/font.ttf", 35)
    text = font.render("Правила", 1, (102, 0, 102))
    text_x = 210
    text_y = 300
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (163, 88, 232), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20), 5)
    text = font.render("Об игре", 1, (102, 0, 102))
    text_x = 225
    text_y = 370
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (163, 88, 232), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20), 5)
    text = font.render("Играть", 1, (102, 0, 102))
    text_x = 228
    text_y = 440
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (163, 88, 232), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20), 5)


def draw_text():
    intro_text = ["\nПутешествия Хомяка\n"]
    pygame.display.set_caption('Maze')
    fon = pygame.transform.scale(load_image('start.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    text_coord = 60
    font = pygame.font.Font("data/font.ttf", 27)
    string_rendered = font.render(intro_text[0], 1, (92, 30, 50))
    intro_rect = string_rendered.get_rect()
    text_coord += 40
    intro_rect.top = text_coord
    intro_rect.x = 120
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)


def draw_count(have, all_balls):
    intro_text = ["\nСобрано: \n",
                  have + "/" + all_balls]
    text_coord = 10
    font = pygame.font.Font("data/font.ttf", 27)
    string_rendered = font.render(intro_text[0], 1, (102, 0, 102))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 447
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    for line in intro_text[1:]:
        font = pygame.font.Font("data/font.ttf", 25)
        string_rendered = font.render(line, 1, (102, 0, 102))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 560
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def start_screen():
    flag_1 = False
    flag_2 = False
    flag_3 = False
    while True:
        if flag_1:
            pygame.draw.rect(screen, (56, 0, 102), (210 - 10, 300 - 10,
                                                    189 + 20, 36 + 20), 5)
            pygame.display.flip()
        elif flag_2:
            pygame.draw.rect(screen, (56, 0, 102), (225 - 10, 370 - 10,
                                                    160 + 20, 36 + 20), 5)
            pygame.display.flip()
        elif flag_3:
            pygame.draw.rect(screen, (56, 0, 102), (228 - 10, 440 - 10,
                                                    149 + 20, 36 + 20), 5)
            pygame.display.flip()
        draw_text()
        draw_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 210 <= x <= 419 and 290 <= y <= 356:
                    rules()
                elif 225 <= x <= 404 and 360 <= y <= 426:
                    info()
                elif 218 <= x <= 386 and 420 <= y <= 486:
                    return
            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                if 210 <= x <= 419 and 290 <= y <= 356:
                    flag_1 = True
                    pygame.draw.rect(screen, (56, 0, 102), (210 - 10, 300 - 10,
                                                            189 + 20, 36 + 20), 5)
                    pygame.display.flip()
                    flag_2 = False
                    flag_3 = False
                elif 225 <= x <= 404 and 360 <= y <= 426:
                    flag_2 = True
                    pygame.draw.rect(screen, (163, 88, 232), (225 - 10, 370 - 10,
                                                              160 + 20, 36 + 20), 5)
                    pygame.display.flip()
                    flag_1 = False
                    flag_3 = False
                elif 218 <= x <= 386 and 420 <= y <= 486:
                    flag_3 = True
                    pygame.draw.rect(screen, (163, 88, 232), (228 - 10, 440 - 10,
                                                              149 + 20, 36 + 20), 5)
                    pygame.display.flip()
                    flag_1 = False
                    flag_2 = False
                else:
                    flag_1 = False
                    flag_2 = False
                    flag_3 = False
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('box.png'),
               'empty': load_image('carpet.png'),
               'ball': load_image('ball.png')}
player_image = load_image('hamster.png')

tile_width = tile_height = 50

tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
balls_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
balls = []


def generate_level(level):
    ball_amount = 0
    ball_dict = {}
    screen.fill((0, 0, 0))
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('empty', x, y)
            elif level[y][x] == '.':
                Wall(x, y)
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                balls.append(Ball(x, y))
                ball_amount += 1
                ball_dict[(x, y)] = True
            pygame.display.flip()
    return new_player, x, y, ball_amount, ball_dict


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images["wall"]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, balls_group)
        self.image = tile_images["ball"]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)

    def check(self):
        if pygame.sprite.spritecollideany(self, player_group):
            all_sprites.remove(self)
            tiles_group.remove(self)
            balls_group.remove(self)
            self.kill()
            balls_group.draw(screen)
            return 1
        return 0


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def check(self):
        if pygame.sprite.spritecollideany(self, wall_group):
            return True
        return False


pygame.display.set_caption('Maze')
taken = 0
END = 10
maze(1, 1, 2)
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_screen()
player, level_x, level_y, amount, ball_dict = \
    generate_level(load_level('map.txt'))
total = amount
tiles_group.draw(screen)
player_group.draw(screen)
balls_group.draw(screen)
pygame.display.flip()

level = 1
flag = False
time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S").split()[1]
sec = int(time.split(":")[0]) * 3600 + int(time.split(":")[1]) * 60 + int(time.split(":")[2])
running = True
duration = 0
while running:
    draw_count(str(taken), str(amount))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            from stars import end_screen
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if 50 <= player.rect.x:
                    tiles_group.draw(screen)
                    player.rect.x -= 50
                    if player.check():
                        player.rect.x += 50
                    player_group.draw(screen)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if player.rect.x < 600:
                    tiles_group.draw(screen)
                    player.rect.x += 50
                    if player.check():
                        player.rect.x -= 50
                    player_group.draw(screen)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if 50 <= player.rect.y:
                    tiles_group.draw(screen)
                    player.rect.y -= 50
                    if player.check():
                        player.rect.y += 50
                    player_group.draw(screen)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if player.rect.y < 600:
                    tiles_group.draw(screen)
                    player.rect.y += 50
                    if player.check():
                        player.rect.y -= 50
                    player_group.draw(screen)
            balls_group.draw(screen)
            player_group.draw(screen)
    for elem in balls:
        taken += elem.check()
        if elem.check() == 1:
            balls.remove(elem)
    if not balls:
        level += 1
        if level >= END:
            time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S").split()[1]
            new_time = int(time.split(":")[0]) * 3600 + int(time.split(":")[1]) * 60 + int(time.split(":")[2])
            duration = new_time - sec
            print(duration)
            fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            running = False
        else:
            taken = 0
            draw_count(str(taken), str(amount))
            all_sprites = pygame.sprite.Group()
            tiles_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            balls_group = pygame.sprite.Group()
            wall_group = pygame.sprite.Group()
            balls = []
            if level == 2:
                maze(2, 2, 4)
            elif level == 3:
                maze(3, 3, 4)
            elif level == 4:
                maze(3, 3, 4)
            elif level == 5:
                maze(3, 3, 5)
            elif level == 6:
                maze(3, 3, 6)
            elif level == 7:
                maze(3, 3, 6)
            elif level == 8:
                maze(4, 4, 6)
            elif level == 9:
                maze(4, 6, 7)
            elif level == 10:
                maze(5, 7, 9)
            screen = pygame.display.set_mode(size)
            screen.fill((0, 0, 0))
            player, level_x, level_y, amount, ball_dict = \
                generate_level(load_level('map.txt'))
            total = amount
            tiles_group.draw(screen)
            player_group.draw(screen)
            balls_group.draw(screen)
            pygame.display.flip()
    pygame.display.flip()

end_screen(duration)
