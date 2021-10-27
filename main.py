# DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
pygame.init()
WIN = pygame.display.set_mode((700, 850), pygame.RESIZABLE)
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
        self.image = pygame.Surface((400, 400))
        self.image.fill((0, 60, 100))
        self.win_center = [350, 0]
        self.rect = self.image.get_rect(midtop=self.win_center)

    def recenter(self):
        self.rect = self.image.get_rect(midtop=self.win_center)

    def update(self):
        self.image.fill((0, 60, 100))
        self.rect.top += 0


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
        self.mask = pygame.mask.from_surface(self.image)


class Raccoon(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, blocks, trash):
        super().__init__()
        self.image = image
        self.pos = start_pos
        self.rect = self.image.get_rect(topleft=(self.pos[0]*40, self.pos[1]*40))
        self.blocks = blocks
        self.trash = trash
        self.movement = 2

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.movement
        if keys[pygame.K_s]:
            self.rect.y += self.movement
        if keys[pygame.K_d]:
            self.rect.x += self.movement
        if keys[pygame.K_a]:
            self.rect.x -= self.movement

    def collisions(self): # shorten
        """make it so when the thing collides the side it collides with = the side on the rect of the block"""

        if pygame.sprite.spritecollide(self, self.blocks, False):
            self.movement = 0

        if pygame.sprite.spritecollide(self, self.trash, False):
            self.movement = 0
            print("you win")

    def update(self):
        self.move()
        self.collisions()


# Eventual Level design
one = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 3, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 2
    ]

blocks_list = []
raccoon_pos = []
trash_pos = []
x = 0
y = 0
for _ in one:
    if one[x + (y*10)] == 1:

        blocks_list.append([x, y])

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
mazegrp = pygame.sprite.GroupSingle(maze)
trash = pygame.sprite.GroupSingle(MazeTrash(TRASH_IMAGE, trash_pos))
maze_blocks = pygame.sprite.Group()
for c in blocks_list:
    maze_blocks.add(MazeBlock(c))
raccoon = pygame.sprite.Group(Raccoon(RACCOON_IMAGE, raccoon_pos, maze_blocks, trash))

# Game Loop
while True:
    CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            maze.win_center[0] = WIN.get_width()/2
            maze.recenter()

    WIN.fill((255, 255, 255))

    mazegrp.draw(WIN)
    mazegrp.update()
    trash.draw(maze.image)
    maze_blocks.draw(maze.image)
    raccoon.draw(maze.image)


    raccoon.update()

    pygame.display.flip()
