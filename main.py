# DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
pygame.init()
win = pygame.display.set_mode((700, 600), pygame.RESIZABLE)
pygame.display.set_caption("Racoonundrum - a trashy game")
clock = pygame.time.Clock()

# Sprite Art
raccoon_image = pygame.transform.scale(pygame.image.load("assets/raccoon.png"), (40, 40))

# Classes


class MazeBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x = pos[0] * 40
        self.y = pos[1] * 40
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 250, 35))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        pass
        # collisions


class Player(pygame.sprite.Sprite):
    def __init__(self, image, surf_rect):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=[400, 0])
        self.pos_y = surf_rect.y
        self.speed_y = 0
        self.gravity_value = 9.8

    def gravity(self):
        self.speed_y += self.gravity_value/60
        self.pos_y += self.speed_y
        self.rect.y = self.pos_y

    def update(self):
        self.gravity()


class MazeSurf(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.first_image = pygame.Surface((400, 400), pygame.SRCALPHA)
        self.image = self.first_image
        self.image.fill((200, 100, 39))
        self.win_center = [350, 300]
        self.rect = self.image.get_rect(center=self.win_center)
        self.angle = 0

    def recenter(self):
        self.rect = self.image.get_rect(center=self.win_center)

    def rotate(self, angle):
        self.image = pygame.transform.rotozoom(self.first_image, self.angle, 1)
        self.angle += angle
        self.recenter()

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rotate(2)
        if key[pygame.K_d]:
            self.rotate(-2)


# Levels
one = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for block in one:
    pass


# Objects
maze = MazeSurf()
block1 = MazeBlock([7,6])
block2 = MazeBlock([9,9])
block3 = MazeBlock([1,1])
raccoon = Player(raccoon_image, maze.rect)
sprites = pygame.sprite.Group(maze, raccoon)
maze_blocks = pygame.sprite.Group(block1, block2, block3)

# Game Loop
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            maze.win_center = [win.get_width()/2, win.get_height()/2]
            maze.recenter()

    win.fill((255, 255, 255))
    maze_blocks.draw(maze.image)
    sprites.draw(win)
    sprites.update()

    pygame.display.flip()
