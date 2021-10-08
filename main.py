# DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
pygame.init()
win_width, win_length = 1100, 750
win = pygame.display.set_mode((win_width, win_length), pygame.RESIZABLE)
pygame.display.set_caption("Racoonundrum - a trashy game")
clock = pygame.time.Clock()

# Sprite Art
raccoon_image = pygame.image.load("assets/raccoon.png")

# Classes


class Surf:
    def __init__(self):
        self.cube_image_1st = pygame.Surface((400, 400), pygame.SRCALPHA)  # cubesurf
        self.cube_image = self.cube_image_1st
        self.cube_image.fill((200, 100, 39))
        self.cube_rect = self.cube_image.get_rect(center=[win_width/2, win_length/2])
        self.angle = 0

    def resize(self):
        self.cube_rect = self.cube_image.get_rect(center=[win_width / 2, win_length / 2])

    def rotate(self, angle):
        self.cube_image = pygame.transform.rotozoom(self.cube_image_1st, self.angle, 1)
        self.angle += angle
        self.resize()

    def update(self):
        win.blit(self.cube_image, self.cube_rect)

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rotate(2)
        if key[pygame.K_d]:
            self.rotate(-2)


class MazeBlock:
    def __init__(self, y, x):
        self.x = x * 40
        self.y = y * 40
        self.size = 40
        self.color = (255, 0, 0)

    def update(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))


cube = Surf()
cube_rect = cube.cube_rect


class FreeFalling:
    def __init__(self, image):
        self.image = image
        self.image_rect = self.image.get_rect(center=[450, 250])
        self.cube_rect = cube_rect
        self.pos_y = 450
        self.speed_y = 0
        self.gravity_value = 1

    def gravity(self):
        if self.cube_rect.contains(self.image_rect):
            self.speed_y += self.gravity_value/120
            self.pos_y += self.speed_y
            self.image_rect.y = self.pos_y
        else:
            self.gravity_value = 0

    def update(self):
        self.gravity()
        win.blit(self.image, (450, 250))


# Objects
raccoon = FreeFalling(raccoon_image)
block1 = MazeBlock(0, 1)
block2 = MazeBlock(0, 2)

# Game Loop
while True:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            cube.resize()
            print("boop")

    win.fill((255, 255, 255))
    cube.update()
    raccoon.update()
    block1, block2.update()

    pygame.display.flip()
