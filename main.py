 # DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
pygame.init()
WIN = pygame.display.set_mode((700, 850), pygame.RESIZABLE)
pygame.display.set_caption("Racoonundrum - a trashy game")

# Constants
CLOCK = pygame.time.Clock()
CENTER = [350, 0]
FILL = (200, 0, 0)
BLOCKS = []
RACCOON_POS = []
TRASH_POS = []
TITLE = True

# Sprite Art
MAZE_IMAGE = pygame.transform.scale(pygame.image.load("assets/block.jpg"), (400, 400))
BLOCK_IMAGE = pygame.transform.scale(pygame.image.load("assets/block.jpg"), (40, 40))
RACCOON_IMAGE = pygame.transform.scale(pygame.image.load("assets/raccoon.png"), (30, 30))
TRASH_IMAGE = pygame.transform.scale(pygame.image.load("assets/trash.png"), (40, 40))


# Classes
class MazeSurf(object):
    def __init__(self):
        self.image = MAZE_IMAGE
        self.rect = self.image.get_rect(midtop=CENTER)

    def fill(self, color):
        self.image.fill((color))

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def recenter(self):
        self.rect = self.image.get_rect(midtop=CENTER)

    def move(self):
        self.rect.top += 0


class Raccoon(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        self.image = RACCOON_IMAGE
        self.rect = pygame.Rect(pos[0]*40, pos[1]*40, 30, 30)

    def move_collide(self, vel_x, vel_y):
        self.rect.x += vel_x
        self.rect.y += vel_y

        if self.rect.right > 400:
            self.rect.right = 400
        if self.rect.bottom > 400:
            self.rect.bottom = 400
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

        if self.rect.colliderect(trash.rect):
            print("boop")


class MazeBlock(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        BLOCKS.append(self)
        self.image = BLOCK_IMAGE
        self.rect = pygame.Rect(pos[0]*40, pos[1]*40, 40, 40)


class MazeTrash(MazeSurf):
    def __init__(self, pos):
        super().__init__()
        self.image = TRASH_IMAGE
        self.rect = pygame.Rect(pos[0]*40, pos[1]*40, 40, 40)


# Eventual Level design
one = [
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
    1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    1, 0, 0, 1, 3, 0, 1, 1, 1, 1,
    1, 0, 0, 1, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 1, 0, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 2
    ]

x = 0
y = 0
for _ in one:
    if one[x + (y*10)] == 1:
        MazeBlock((x, y))

    if one[x + (y*10)] == 2:
        RACCOON_POS = [x, y]

    if one[x + (y*10)] == 3:
        TRASH_POS = [x, y]

    x += 1
    if x > 9:
        x = 0
        y += 1


# Objects
maze = MazeSurf()
raccoon = Raccoon(RACCOON_POS)
trash = MazeTrash(TRASH_POS)

# Game Loop
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            TITLE = False
            break
        pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        raccoon.move_collide(0, -2)
    if keys[pygame.K_s]:
        raccoon.move_collide(0, 2)
    if keys[pygame.K_d]:
        raccoon.move_collide(2, 0)
    if keys[pygame.K_a]:
        raccoon.move_collide(-2, 0)

    WIN.fill((255, 255, 255))
    maze.draw(WIN)
    maze.fill(FILL)
    for b in BLOCKS:
        b.draw(maze.image)
    raccoon.draw(maze.image)
    trash.draw(maze.image)
    maze.move()

    pygame.display.flip()
