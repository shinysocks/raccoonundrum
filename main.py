# DEDICATED TO EMILY

# Initial Setup
import pygame
from random import randint
from sys import exit
from time import sleep
pygame.init()
WIN = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Racoonundrum - a trashy game")

# Constants
CLOCK = pygame.time.Clock()
BLOCKS, RATS = [], []
SIZE = 70

# Sprite Art
BLOCK_IMAGES = [
    pygame.transform.scale(pygame.image.load("assets/block0.jpg"), (70, 70)),
    pygame.transform.scale(pygame.image.load("assets/block1.jpg"), (70, 70)),
    pygame.transform.scale(pygame.image.load("assets/block2.jpg"), (70, 70)),
    pygame.transform.scale(pygame.image.load("assets/block3.jpg"), (70, 70)),
    ]

RACCOON_IMAGES = [
    pygame.image.load("assets/raccoon0.jpg"),
    pygame.image.load("assets/raccoon1.jpg"),
    pygame.image.load("assets/raccoon2.jpg"),
    pygame.image.load("assets/raccoon3.jpg"),
    ]

TRASH_IMAGES = [
    pygame.image.load("assets/trash0.png"),
    pygame.image.load("assets/trash1.png"),
    pygame.image.load("assets/trash2.png"),
    pygame.image.load("assets/trash3.png"),
    pygame.image.load("assets/trash4.png"),
    ]

RAT_IMAGES = [
    pygame.transform.rotate(pygame.image.load("assets/rats0.png"), 180),
    pygame.transform.rotate(pygame.image.load("assets/rats1.png"), 0),
    pygame.transform.rotate(pygame.image.load("assets/rats0.png"), 270),
    pygame.transform.rotate(pygame.image.load("assets/rats1.png"), 90),
    ]


# Classes
class MazeSurf(object):
    def __init__(self):
        self.image = pygame.Surface((700, 700))
        self.rect = self.image.get_rect()
        self.rect.x += 10
        self.rect.y += 10

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Raccoon(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        self.image = RACCOON_IMAGES[2]
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 45, 45)
        self.rect.x += 12
        self.rect.y += 12

    def update(self, vel_x, vel_y):
        self.rect.x += vel_x
        self.rect.y += vel_y

        if self.rect.right > 700:
            self.rect.right = 700
        if self.rect.bottom > 700:
            self.rect.bottom = 700
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


class MazeTrash(Raccoon):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = TRASH_IMAGES[0]
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 45, 45)
        self.rect.x += 12
        self.rect.y += 12

    def collide(self):
        if self.rect.colliderect(raccoon.rect):
            level.lev_up()


class MazeBlock(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        BLOCKS.append(self)
        self.image = BLOCK_IMAGES[randint(0, 3)]
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, SIZE, SIZE)


class MazeRat(MazeSurf):
    def __init__(self, pos, rat_type):
        super().__init__()
        RATS.append(self)
        self.image = RAT_IMAGES[0]
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 70, 70)
        self.hitrect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 40, 55)
        self.hitrect.center = self.rect.center
        self.vel = 4
        self.rat_type = rat_type

    def update(self):
        if self.rat_type == 1:
            self.rect.x += self.vel
            self.hitrect.x += self.vel
            if self.vel == -4:
                self.image = RAT_IMAGES[2]
            else:
                self.image = RAT_IMAGES[3]

        if self.rat_type == 2:
            if self.vel == -4:
                self.image = RAT_IMAGES[0]
            else:
                self.image = RAT_IMAGES[1]
            self.rect.y += self.vel
            self.hitrect.y += self.vel

        for block in BLOCKS:
            if self.rect.colliderect(block.rect):
                self.vel *= -1

        if self.rect.left <= 0 or self.rect.right >= 700:
            self.vel *= -1

        if self.rect.top <= 0 or self.rect.bottom >= 700:
            self.vel *= -1

        if self.hitrect.colliderect(trash.rect):
            level.restart()

        if self.hitrect.colliderect(raccoon.rect):
            level.restart()

            
class Level(object):
    def __init__(self):
        self.level_num = 1
        self.blocks = BLOCKS
        self.rats = RATS
        self.levels = {
                1: [
                    1, 1, 1, 0, 1, 1, 5, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 3, 0, 0, 0, 0, 0, 0, 0, 1,
                    1, 1, 1, 5, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 0, 0, 0, 0, 2, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    ],

                2: [
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    4, 0, 0, 0, 0, 0, 0, 4, 0, 0,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    2, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                    1, 1, 1, 1, 1, 1, 1, 5, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    ],

                3: [
                    0, 0, 5, 0, 5, 0, 5, 0, 5, 3,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 4, 0, 0, 0, 0,
                    0, 0, 1, 0, 0, 4, 0, 1, 0, 0,
                    0, 0, 1, 0, 0, 4, 0, 1, 0, 0,
                    0, 0, 0, 0, 0, 4, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 5, 0, 5, 0, 5, 0, 5, 0, 0,
                    2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    ]
                    }

    def generate(self, lev_list):
        global raccoon, trash
        self.blocks.clear()
        self.rats.clear()
        x = 0
        y = 0
        for _ in lev_list:
            if lev_list[x + (y*10)] == 1:
                MazeBlock((x, y))

            if lev_list[x + (y*10)] == 2:
                raccoon = Raccoon([x, y])

            if lev_list[x + (y*10)] == 3:
                trash = MazeTrash([x, y])

            if lev_list[x + (y*10)] == 4:
                MazeRat([x, y], 1)

            if lev_list[x + (y*10)] == 5:
                MazeRat([x, y], 2)
            
            x += 1
            if x > 9:
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
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        raccoon.image = RACCOON_IMAGES[0]
        trash.image = TRASH_IMAGES[1]
        raccoon.update(-3, 0)
        trash.update(3, 0)

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        raccoon.image = RACCOON_IMAGES[1]
        trash.image = TRASH_IMAGES[2]
        raccoon.update(3, 0)
        trash.update(-3, 0)

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        raccoon.image = RACCOON_IMAGES[2]
        trash.image = TRASH_IMAGES[3]
        raccoon.update(0, -3)
        trash.update(0, 3)
        
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        raccoon.image = RACCOON_IMAGES[3]
        trash.image = TRASH_IMAGES[4]
        raccoon.update(0, 3)
        trash.update(0, -3)

    WIN.fill((255, 255, 255))
    maze.draw(WIN)
    maze.image.fill((255, 255, 255))

    for b in BLOCKS:
        b.draw(maze.image)

    for r in RATS:
        r.draw(maze.image)
        r.update()

    raccoon.draw(maze.image)
    trash.draw(maze.image)
    trash.collide()
    
    pygame.display.flip()
