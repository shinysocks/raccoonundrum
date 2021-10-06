### DEDICATED TO EMILY ###
#boopity doop
#Initial Setup
import pygame
from sys import exit
pygame.init()
display = pygame.display.set_mode((900,700))
pygame.display.set_caption("Racoonundrum - a trashy game")
clock = pygame.time.Clock()

#Classes
class Cube(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.Surface((300,300), pygame.SRCALPHA)
        self.image = self.image1
        self.image.fill((200,100,39))
        self.rect = self.image.get_rect(center=[450,350])
        self.angle = 0
    
    def rotate(self, angle):
            self.image = pygame.transform.rotozoom(self.image1, self.angle,1)
            self.angle += angle 
            self.rect = self.image.get_rect(center=[450,350]) 

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rotate(1)
        if key[pygame.K_d]:
            self.rotate(-1)


class FreeFalling(pygame.sprite.Sprite):
    def __init__(self,image,center):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center)
        self.pos_y = center[1]
        self.speed_y = 0
        self.gravity = 1

    def update(self):
        if self.rect.bottom >= 400:
            self.speed_y = 0
        else:
            self.speed_y += self.gravity/120
            self.pos_y += self.speed_y
            self.rect.y = self.pos_y

class Level():
    pass


#Sprites Group
cube = Cube()
raccoon = FreeFalling(pygame.image.load("assets/raccoon.png"), [450,300])

sprites_group = pygame.sprite.Group()
sprites_group.add(cube,raccoon)

#Game Loop
while True:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    display.fill((23,34,120))
    sprites_group.draw(display)
    sprites_group.update()
    pygame.display.flip()
