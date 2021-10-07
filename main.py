# DEDICATED TO EMILY

# Initial Setup
import pygame
from sys import exit
pygame.init()
display = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Racoonundrum - a trashy game")
clock = pygame.time.Clock()

# Sprite Art
raccoon_image = pygame.image.load("assets/raccoon.png")


# Classes
class Cube:
    def __init__(self):
        self.cube_image_1st = pygame.Surface((300, 300), pygame.SRCALPHA)
        self.cube_image = self.cube_image_1st
        self.cube_image.fill((200, 100, 39))
        self.cube_rect = self.cube_image.get_rect(center=[450, 350])
        self.angle = 0
    
    def rotate(self, angle):
        self.cube_image = pygame.transform.rotozoom(self.cube_image_1st, self.angle, 1)
        self.angle += angle
        self.cube_rect = self.cube_image.get_rect(center=[450, 350])

    def update(self):
        display.blit(self.cube_image, (450, 350))

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rotate(2)
        if key[pygame.K_d]:
            self.rotate(-2)


cube = Cube()
cube_rect = cube.cube_rect


class FreeFalling:
    def __init__(self, image):
        self.image = image
        self.image_rect = self.image.get_rect(center=[450, 250])
        self.cube_rect = cube_rect
        self.pos_y = 450
        self.speed_y = 0
        self.gravity = 1

    def apply_gravity(self):
        self.speed_y += self.gravity/120
        self.pos_y += self.speed_y
        self.image_rect.y = self.pos_y

    def update(self):
        display.blit(self.image, (450, 250))

        if not self.cube_rect.contains(self.image_rect):
            self.speed_y = 0
        else:
            self.apply_gravity()


raccoon = FreeFalling(raccoon_image)

# Game Loop
while True:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    display.fill((23, 34, 120))
    cube.update()
    raccoon.update()
    pygame.display.flip()
