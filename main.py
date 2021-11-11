# DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
from time import sleep
pygame.init()
WIN = pygame.display.set_mode((750, 750))
pygame.display.set_caption("Racoonundrum - a trashy game")

# Constants
CLOCK = pygame.time.Clock()
FILL = (200, 0, 0)
BLOCKS, RATS = [], []
SIZE = 50

# Sprite Art
RACCOON_LOAD = pygame.transform.scale(pygame.image.load("assets/raccoon.png"), (40, 40))
MAZE_IMAGE = pygame.transform.scale(pygame.image.load("assets/block.jpg"), (750, 750))
BLOCK_IMAGE = pygame.transform.scale(pygame.image.load("assets/block.jpg"), (50, 50))
RACCOON_IMAGES = [
    pygame.transform.rotate(RACCOON_LOAD, 0),
    pygame.transform.rotate(RACCOON_LOAD, 90),
    pygame.transform.rotate(RACCOON_LOAD, 180),
    pygame.transform.rotate(RACCOON_LOAD, 270)
    ]
TRASH_IMAGE = pygame.transform.scale(pygame.image.load("assets/trash.png"), (50, 50))
RAT_IMAGE = pygame.transform.scale(pygame.image.load("assets/rat.png"), (50, 50))


# Classes
class MazeSurf(object):
    def __init__(self):
        self.image = MAZE_IMAGE
        self.rect = self.image.get_rect()

    def fill(self, color):  # to be removed
        self.image.fill(color)

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Raccoon(object):
    def __init__(self, pos):
        self.image = RACCOON_IMAGES[0]
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 40, 40)

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def move(self, vel_x, vel_y):
        self.rect.x += vel_x
        self.rect.y += vel_y

        if self.rect.right > 750:
            self.rect.right = 750
        if self.rect.bottom > 750:
            self.rect.bottom = 750
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0

        for block in BLOCKS:
            if self.rect.colliderect(block.rect):
                if vel_x > 0:
                    self.rect.right = block.rect.left
                if vel_x < 0:
                    self.rect.left = block.rect.right
                if vel_y > 0:
                    self.rect.bottom = block.rect.top
                if vel_y < 0:
                    self.rect.top = block.rect.bottom

    def collide(self):
        if self.rect.colliderect(trash.rect):
            level.lev_up()
        for rat in RATS:
            if self.rect.colliderect(rat.rect):
                level.restart()


class MazeTrash(Raccoon):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = TRASH_IMAGE
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 50, 50)


class MazeBlock(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        BLOCKS.append(self)
        self.image = BLOCK_IMAGE
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, SIZE, SIZE)


class MazeRat(MazeSurf):
    def __init__(self, pos, rat_type):
        super().__init__()
        RATS.append(self)
        self.image = RAT_IMAGE
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 50, 50)
        self.vel = 4
        self.rat_type = rat_type

    def move(self):
        if self.rat_type == 1:
            self.rect.x += self.vel
        if self.rat_type == 2:
            self.rect.y += self.vel
        
        if self.rect.left >= 750 or self.rect.right <= 0:
            self.vel *= -1
        if self.rect.top >= 750 or self.rect.bottom <= 0:
            self.vel *= -1

        for block in BLOCKS:
            if self.rect.colliderect(block.rect):
                self.vel *= -1
        if self.rect.colliderect(trash.rect):
            level.restart()

            
class Level(object):
    def __init__(self):
        self.level_num = 1
        self.blocks = BLOCKS
        self.rats = RATS
        self.levels = {
                1: [
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 3, 0, 0, 0, 0, 5, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 5, 0, 0, 0, 0, 2, 1,
                    1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1
                    ],

                2: [
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 3, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 2, 5, 0, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
                    ]
                    }

    def generate(self, lev_list):
        global raccoon, trash
        self.blocks.clear()
        self.rats.clear()
        x = 0
        y = 0
        for _ in lev_list:
            if lev_list[x + (y*15)] == 1:
                MazeBlock((x, y))

            if lev_list[x + (y*15)] == 2:
                raccoon = Raccoon([x, y])

            if lev_list[x + (y*15)] == 3:
                trash = MazeTrash([x, y])

            if lev_list[x + (y*15)] == 4:
                MazeRat([x, y], 1)

            if lev_list[x + (y*15)] == 5:
                MazeRat([x, y], 2)
            
            x += 1
            if x > 14:
                x = 0
                y += 1
    
    def lev_up(self):
        WIN.fill((0, 255, 0))
        pygame.display.flip()
        sleep(2)
        self.level_num += 1
        try:
            self.generate(self.levels[self.level_num])
        except KeyError:
            WIN.fill((0, 0, 0))
            pygame.display.flip()
            sleep(3)
            exit()

    def restart(self):
        self.generate(self.levels[self.level_num])


# Objects
level = Level()
maze = MazeSurf()
level.generate(level.levels[1])

# Game Loop
TITLE = True
while True:
    CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Title Screen
    while TITLE:
        WIN.fill((255, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13:
                    TITLE = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        raccoon.image = RACCOON_IMAGES[0]
        raccoon.move(0, -3)
        trash.move(0, 3)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        raccoon.image = RACCOON_IMAGES[2]
        raccoon.move(0, 3)
        trash.move(0, -3)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        raccoon.image = RACCOON_IMAGES[1]
        raccoon.move(3, 0)
        trash.move(-3, 0)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        raccoon.image = RACCOON_IMAGES[3]
        raccoon.move(-3, 0)
        trash.move(3, 0)

    WIN.fill((255, 255, 255, 0))
    maze.draw(WIN)
    maze.fill(FILL)

    for b in BLOCKS:
        b.draw(maze.image)

    for r in RATS:
        r.draw(maze.image)
        r.move()

    raccoon.draw(maze.image)
    raccoon.collide()
    trash.draw(maze.image)
    
    pygame.display.flip()
