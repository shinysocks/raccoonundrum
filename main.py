# DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
pygame.init()
win_width, win_length = 700, 600
win = pygame.display.set_mode((win_width, win_length), pygame.RESIZABLE)
pygame.display.set_caption("Racoonundrum - a trashy game")
clock = pygame.time.Clock()

# Sprite Art
raccoon_image = pygame.image.load("assets/raccoon.png")
raccoon_image = pygame.transform.scale(raccoon_image, (40, 40))

# Classes


class Level:
    pass


class MazeSurf:
    def __init__(self):
        self.surf1 = pygame.Surface((400, 400), pygame.SRCALPHA)
        self.surf = self.surf1
        self.surf.fill((200, 100, 39))
        self.win_center = [win_width/2, win_length/2]
        self.surf_rect = self.surf.get_rect(center=self.win_center)
        self.angle = 0

    def rotate(self, angle):
        self.surf = pygame.transform.rotozoom(self.surf1, self.angle, 1)
        self.angle += angle
        self.surf_rect = self.surf.get_rect(center=self.win_center)

    def update(self):
        win.blit(self.surf, self.surf_rect)

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rotate(2)
        if key[pygame.K_d]:
            self.rotate(-2)


class MazeBlock:
    def __init__(self, y, x, maze_surf):
        self.x = x * 40
        self.y = y * 40
        self.size = 40
        self.color = (255, 0, 0)
        self.maze_surf = maze_surf

    def update(self):
        pygame.draw.rect(self.maze_surf, self.color, (self.x, self.y, self.size, self.size))


class Player:
    def __init__(self, image, surf_rect):
        self.image = image
        self.image_rect = self.image.get_rect(center=[400, 0])
        self.pos_y = surf_rect.y
        self.speed_y = 1
        self.gravity_value = 9.8

    def gravity(self):
        self.speed_y += self.gravity_value/60
        self.pos_y += self.speed_y
        self.image_rect.y = self.pos_y

    def update(self):
        win.blit(self.image, self.image_rect)
        self.gravity()


# Objects

maze = MazeSurf()
block1 = MazeBlock(7, 5, maze.surf)
block2 = MazeBlock(7, 6, maze.surf)
block3 = MazeBlock(1, 1, maze.surf)
raccoon = Player(raccoon_image, maze.surf_rect)
game_objects = [maze, raccoon, block1, block2, block3]

# Game Loop
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            win_width, win_length = win_width, win_length
            cube.win_center = [win_width/2, win_length/2] # fix this

    win.fill((255, 255, 255))
    for obj in game_objects:
        obj.update()

    pygame.display.flip()
