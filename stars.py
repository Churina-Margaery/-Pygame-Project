import pygame
import random
import os
import sys


pygame.init()
GRAVITY = -0.008
width = 650
height = 650
screen_rect = (0, 0, width, height)
all_sprites = pygame.sprite.Group()
pygame.display.set_caption('Maze')


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
        super().__init__(all_sprites)
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


def end_screen():
    pygame.display.set_caption('Maze')
    size = width, height
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
        fon = pygame.transform.scale(load_image('fon.jpg'), size)
        screen.blit(fon, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)


end_screen()
pygame.quit()
