# DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
pygame.init()
WIN = pygame.display.set_mode((700, 600), pygame.RESIZABLE)
pygame.display.set_caption("Racoonundrum - a trashy game")
CLOCK = pygame.time.Clock()

# Sprite Art
raccoon_load = pygame.image.load("assets/raccoon.png")
trash_load = pygame.image.load("assets/trash.png")
RACCOON_IMAGE = pygame.transform.scale(raccoon_load, (40, 40))
TRASH_IMAGE = pygame.transform.scale(trash_load, (40, 40))

# Classes


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
        if self.angle < 0:
            self.angle = 360
        if self.angle > 360:
            self.angle = 0
        self.recenter()

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rotate(2)
        if key[pygame.K_d]:
            self.rotate(-2)


class MazeBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 250, 35))
        self.rect = self.image.get_rect(topleft=(pos[0]*40, pos[1]*40))


class MazeTrash(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(pos[0]*40, pos[1]*40))


class Raccoon(pygame.sprite.Sprite):
    def __init__(self, image, pos, blocks):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(pos[0]*40, pos[1]*40))
        self.pos_y = pos[1]*40
        self.speed_y = 1
        self.gravity_value = 1
        self.blocks = blocks

    def gravity(self):
        self.speed_y += self.gravity_value/60
        self.pos_y += self.speed_y
        self.rect.y = self.pos_y

    def collide(self):
        listy = pygame.sprite.spritecollide(self, self.blocks, False)
        print(listy)

    def update(self):
        self.gravity()
        self.collide()


# Levels
one = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 3, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]

# Not Sure Yet


blocks = []

x = 0
y = 0
for _ in one:
    if one[x + (y*10)] == 1:

        blocks.append([x, y])

    if one[x + (y*10)] == 2:
        raccoon_pos = [x, y]

    if one[x + (y*10)] == 3:
        trash_pos = [x, y]
    
    x += 1
    if x > 9:
        x = 0
        y += 1


# Objects
maze = MazeSurf()
maze_blocks = pygame.sprite.Group()
for c in blocks:
    maze_blocks.add(MazeBlock(c))

trash = pygame.sprite.Group(MazeTrash(TRASH_IMAGE, trash_pos))
raccoon = Raccoon(RACCOON_IMAGE, raccoon_pos, maze_blocks)
sprites = pygame.sprite.Group(maze, raccoon)

maze_blocks.draw(maze.image)
trash.draw(maze.image)

print(maze_blocks)
# Game Loop
while True:
    CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            maze.win_center = [win.get_width()/2, win.get_height()/2]
            maze.recenter()

    WIN.fill((255, 255, 255))
    sprites.draw(WIN)
    sprites.update()

    pygame.display.flip()
