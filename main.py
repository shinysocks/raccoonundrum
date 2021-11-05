 # DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
from time import sleep
pygame.init()
WIN = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Racoonundrum - a trashy game")

# Constants
CLOCK = pygame.time.Clock()
FILL = (200, 0, 0)
BLOCKS = []
ENEMIES = []
CUBE_SIZE = 40

# Sprite Art
MAZE_IMAGE = pygame.transform.scale(pygame.image.load("assets/block.jpg"), (600, 600))
BLOCK_IMAGE = pygame.transform.scale(pygame.image.load("assets/block.jpg"), (40, 40))
RACCOON_IMAGE = pygame.transform.scale(pygame.image.load("assets/raccoon.png"), (36, 33))
TRASH_IMAGE = pygame.transform.scale(pygame.image.load("assets/trash.png"), (40, 40))
ENEMY_IMAGE = pygame.transform.scale(pygame.image.load("assets/enemy.png"), (40, 40))


# Classes
class MazeSurf(object):
    def __init__(self):
        self.image = MAZE_IMAGE
        self.rect = self.image.get_rect()

    def fill(self, color):
        self.image.fill((color))

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Raccoon(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        self.image = RACCOON_IMAGE
        self.rect = pygame.Rect(pos[0]*CUBE_SIZE, pos[1]*CUBE_SIZE, 36, 33)

    def move(self, vel_x, vel_y):
        self.rect.x += vel_x
        self.rect.y += vel_y

        if self.rect.right > 600:
            self.rect.right = 600
        if self.rect.bottom > 600:
            self.rect.bottom = 600
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
            level.levelup()
        for enemy in ENEMIES:
            if self.rect.colliderect(enemy.rect):
                level.restart()


class MazeBlock(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        BLOCKS.append(self)
        self.image = BLOCK_IMAGE
        self.rect = pygame.Rect(pos[0]*CUBE_SIZE, pos[1]*CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)


class MazeTrash(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        self.image = TRASH_IMAGE
        self.rect = pygame.Rect(pos[0]*CUBE_SIZE, pos[1]*CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)


class MazeEnemy(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        ENEMIES.append(self)
        self.image = ENEMY_IMAGE
        self.rect = pygame.Rect(pos[0]*CUBE_SIZE, pos[1]*CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        self.vel_x = 6

    def move(self):
        self.rect.x += self.vel_x
        if self.rect.right >= 600:
            self.vel_x = -6
        if self.rect.left <= 0:
            self.vel_x = 6

        for block in BLOCKS:
            if self.rect.colliderect(block.rect):
                if self.vel_x > 0:
                    self.rect.left = block.rect.right
                    self.vel_x = 6
                if self.vel_x < 0:
                    self.rect.right = block.rect.left
                    self.vel_x = -6  

            
class Level(object):
    def __init__(self):
        self.levelnum = 1
        self.levels = {
                1 : ( 
                    0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0,
                    1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0,
                    1, 0, 1, 0, 4, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                    1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0,
                    1, 0, 0, 1, 3, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1,
                    1, 0, 0, 1, 2, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0,
                    1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0,
                    1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1,
                    0, 1, 4, 0, 0, 0, 0, 1, 0, 4, 1, 1, 1, 0, 0,
                    1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 1, 1, 1, 0, 0,
                    1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1,
                    1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0,
                    1, 0, 1, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0,
                    1, 0, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
                    1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0
                    )
                    }

    def generate(self, level, blocks, enemies):
        global raccoon, trash # fix
        blocks = []
        enemies = []
        x = 0
        y = 0
        for _ in level:
            if level[x + (y*15)] == 1:
                MazeBlock((x, y))

            if level[x + (y*15)] == 2:
                raccoon = Raccoon([x, y])

            if level[x + (y*15)] == 3:
                trash = MazeTrash([x, y])

            if level[x + (y*15)] == 4:
                MazeEnemy([x, y])

            x += 1
            if x > 15:
                x = 0
                y += 1
    
    def levelup(self):
        WIN.fill((0, 255, 0))
        pygame.display.flip()
        sleep(2)
        self.levelnum += 1
        try:
            self.generate(self.levels[self.levelnum], BLOCKS, ENEMIES)
        except KeyError:
            WIN.fill((0, 0, 0))
            pygame.display.flip()
            sleep(3)
            exit()

    def restart(self):
        self.generate(self.levels[self.levelnum], BLOCKS, ENEMIES)


# Objects
level = Level()
maze = MazeSurf()
level.generate(level.levels[1], BLOCKS, ENEMIES)

# Game Loop
TITLE = True
while True:
    CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            CENTER[0] = WIN.get_width()/2
            maze.recenter()

    # Title Screen
    while TITLE:
        WIN.fill((255, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                CENTER[0] = WIN.get_width()/2
                maze.recenter()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13:
                    TITLE = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        raccoon.move(0, -3)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        raccoon.move(0, 3)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        raccoon.move(3, 0)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        raccoon.move(-3, 0)

    WIN.fill((255, 255, 255, 0))
    maze.draw(WIN)
    maze.fill(FILL)
    for b in BLOCKS:
        b.draw(maze.image)

    for e in ENEMIES:
        e.draw(maze.image)
        e.move()

    raccoon.draw(maze.image)
    raccoon.collide()
    trash.draw(maze.image)
    
    pygame.display.flip()
