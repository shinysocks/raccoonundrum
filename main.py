'''
    Copyright (c) 2022 Noah Dinan

    This program is free software: you can redistribute it and/or modify  
    it under the terms of the GNU General Public License as published by  
    the Free Software Foundation, version 3.

    This program is distributed in the hope that it will be useful, but 
    WITHOUT ANY WARRANTY; without even the implied warranty of 
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
    General Public License for more details.

    You should have received a copy of the GNU General Public License 
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import pygame
from random import randint
from sys import exit
from time import time, sleep

pygame.init()
win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Raccoonundrum - a trashy game")

# Variables
clock = pygame.time.Clock()
timer = time()
music = pygame.mixer.music
lives = 3
blocks, rats, hearts, sprites = [], [], {}, {}
size = 70
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (40, 40, 40)
titling = True

# Load
music.load("assets/background_music.wav")
title_music = pygame.mixer.Sound("assets/title_theme.wav")
button_sound = pygame.mixer.Sound("assets/button_sound.wav")
death_sound = pygame.mixer.Sound("assets/death_sound.wav")
levelup_sound = pygame.mixer.Sound("assets/complete_sound.wav")
death_image = pygame.image.load("assets/death.jpg")
levelup_image = pygame.image.load("assets/complete.jpg")
font = pygame.font.Font("assets/font.ttf", 50)

# Classes


# Blocks of the maze
class Block:
    def __init__(self, pos):
        blocks.append(self)
        self.images = [
            pygame.image.load("assets/block0.jpg"),
            pygame.image.load("assets/block1.jpg"),
            pygame.image.load("assets/block2.jpg"),
            pygame.image.load("assets/block3.jpg"),
            ]
        self.image = self.images[randint(0, 3)]  # random image chosen
        self.rect = pygame.Rect(pos[0]*size, pos[1]*size, size, size)


# Title animation
class Title:
    def __init__(self, pos):
        self.images = [
            pygame.image.load("assets/title0.jpg"),
            pygame.image.load("assets/title1.jpg"),
            ]
        self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, speed):
        self.current_image += speed
        if int(self.current_image) >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]
        draw(self)


# Start and quit button animation and hovering
class StartButton(Title):
    def __init__(self, pos):
        super().__init__(pos)
        self.hovered = pygame.image.load("assets/start_hover.png")
        self.over = False
        self.images = [
            pygame.image.load("assets/start0.png"),
            pygame.image.load("assets/start1.png"),
            ]
        self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))

    def hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if not self.over:
                button_sound.play(0)
                self.over = True
            self.image = self.hovered
            draw(self)

        if not self.rect.collidepoint(mouse_pos):
            self.over = False
            self.update(.05)


class QuitButton(StartButton):
    def __init__(self, pos):
        super().__init__(pos)
        self.hovered = pygame.image.load("assets/quit_hover.png")
        self.images = [
            pygame.image.load("assets/quit0.png"),
            pygame.image.load("assets/quit1.png"),
            ]


# Raccoon and Trash movement, animation, and collisions
class Raccoon:
    def __init__(self, pos):
        self.images = [
            pygame.image.load("assets/raccoon0.jpg"),
            pygame.image.load("assets/raccoon1.jpg"),
            pygame.image.load("assets/raccoon2.jpg"),
            pygame.image.load("assets/raccoon3.jpg"),
            ]
        self.image = self.images[2]
        self.rect = pygame.Rect(pos[0]*size, pos[1]*size, 45, 45)
        self.rect.x += 12
        self.rect.y += 12
        self.isTrash = False

    def move_collide(self, vel_x, vel_y):
        if self.isTrash:  # Reversed movement
            vel_x *= -1
            vel_y *= -1

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

        for block in blocks:
            if self.rect.colliderect(block.rect):
                if vel_x > 0:
                    self.rect.right = block.rect.left
                if vel_x < 0:
                    self.rect.left = block.rect.right
                if vel_y > 0:
                    self.rect.bottom = block.rect.top
                if vel_y < 0:
                    self.rect.top = block.rect.bottom

    def update(self, pressed):
        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            self.image = self.images[0]
            self.move_collide(-3, 0)

        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.image = self.images[1]
            self.move_collide(3, 0)

        if pressed[pygame.K_w] or pressed[pygame.K_UP]:
            self.image = self.images[2]
            self.move_collide(0, -3)

        if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.image = self.images[3]
            self.move_collide(0, 3)

        draw(self)

# trash can inherits movement from raccoon
class Trash(Raccoon):
    def __init__(self, pos):
        super().__init__(pos)
        self.images = [
            pygame.image.load("assets/trash1.png"),
            pygame.image.load("assets/trash0.png"),
            pygame.image.load("assets/trash3.png"),
            pygame.image.load("assets/trash2.png"),
            ]
        self.image = self.images[2]
        self.rect = pygame.Rect(pos[0]*size, pos[1]*size, 45, 45)
        self.rect.x += 12
        self.rect.y += 12
        self.isTrash = True

    def collide(self):
        if self.rect.colliderect(sprites["raccoon"].rect):
            level.lev_up()


# Enemy maze rats movement up & down + side to side
class RatUp:
    def __init__(self, pos):
        rats.append(self)
        self.images = [
            pygame.transform.rotate(pygame.image.load("assets/rats0.png"), 180),
            pygame.transform.rotate(pygame.image.load("assets/rats1.png"), 0),
            pygame.transform.rotate(pygame.image.load("assets/rats0.png"), 270),
            pygame.transform.rotate(pygame.image.load("assets/rats1.png"), 90),
            ]
        self.image = self.images[0]
        self.rect = pygame.Rect(pos[0]*size, pos[1]*size, 70, 70)
        self.hitrect = pygame.Rect(pos[0]*size, pos[1]*size, 40, 50)
        self.hitrect.center = self.rect.center
        self.vel = 4

    def collide(self):  # collisions
        for block in blocks:
            if self.rect.colliderect(block.rect):
                self.vel *= -1

        if self.rect.left < 0 or self.rect.right > 700:
            self.vel *= -1

        if self.rect.top < 0 or self.rect.bottom > 700:
            self.vel *= -1

        if self.hitrect.colliderect(sprites["trash"].rect):
            level.restart()

        if self.hitrect.colliderect(sprites["raccoon"].rect):
            level.restart()

    def update(self):
        self.rect.y += self.vel
        self.hitrect.y += self.vel
        if self.vel == -4:
            self.image = self.images[0]
        else:
            self.image = self.images[1]

        draw(self)
        self.collide()


class RatSide(RatUp):
    def __init__(self, pos):
        super().__init__(pos)
        rats.append(self)
        self.image = self.images[2]
        self.hitrect = pygame.Rect(pos[0]*size, pos[1]*size, 50, 40)
        self.hitrect.center = self.rect.center
        self.vel = 2

    def update(self):
        self.rect.x += self.vel
        self.hitrect.x += self.vel
        if self.vel == -2:
            self.image = self.images[2]
        else:
            self.image = self.images[3]
        
        draw(self)
        self.collide()


# Hearts animation
class Hearts(Title):
    def __init__(self, pos):
        super().__init__(pos)
        self.images = [
            pygame.image.load("assets/heart0.png"),
            pygame.image.load("assets/heart1.png"),
            ]
        self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect(topleft=pos)


# Level generation and progression
class Level(object):
    def __init__(self):
        self.level_num = 1
        self.sprites = sprites
        self.blocks = blocks
        self.rats = rats
        self.levels = {
                1: [  # tutorial
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    2, 0, 0, 0, 1, 1, 0, 0, 0, 3,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    4, 0, 0, 0, 1, 1, 0, 0, 0, 4,
                    4, 0, 0, 0, 1, 1, 0, 0, 0, 4,
                    1, 1, 1, 0, 0, 0, 0, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    ],

                2: [  # tricky 2
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 0, 3,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    4, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    2, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                    1, 1, 1, 1, 1, 1, 1, 5, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                ],


                3: [  # updownup
                    4, 0, 0, 0, 0, 5, 0, 0, 0, 4,
                    0, 1, 0, 1, 0, 0, 1, 0, 1, 1,
                    0, 1, 0, 1, 0, 0, 1, 0, 1, 1,
                    0, 1, 0, 1, 0, 0, 1, 0, 1, 1,
                    0, 1, 0, 1, 0, 0, 1, 0, 1, 3,
                    2, 1, 0, 1, 0, 0, 1, 0, 1, 0,
                    1, 1, 0, 1, 0, 0, 1, 0, 1, 0,
                    1, 1, 0, 1, 0, 0, 1, 0, 1, 0,
                    1, 1, 0, 1, 0, 0, 1, 0, 1, 0,
                    4, 0, 0, 0, 5, 0, 0, 0, 0, 4,
                ],

                4: [  # tricky
                    0, 0, 0, 2, 0, 1, 0, 5, 0, 0,
                    4, 0, 0, 0, 1, 0, 0, 0, 0, 4,
                    0, 1, 0, 0, 0, 1, 3, 0, 1, 0,
                    4, 0, 0, 0, 1, 0, 0, 0, 0, 4,
                    0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                    4, 0, 0, 0, 1, 0, 0, 0, 0, 4,
                    0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                    4, 0, 0, 0, 1, 0, 0, 0, 0, 4,
                    0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                    0, 0, 5, 0, 0, 0, 0, 0, 0, 4,
                    ],

                5: [  # hashtag
                    1, 1, 1, 5, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 3, 0, 0, 0, 0, 0, 0, 0, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 0, 0, 0, 0, 2, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 5, 1, 1, 1,
                ],


                6: [  # rapunzel
                    0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                    0, 1, 1, 1, 1, 0, 1, 1, 1, 0,
                    0, 1, 0, 0, 0, 4, 1, 2, 0, 0,
                    0, 1, 1, 1, 0, 1, 1, 0, 1, 0,
                    0, 1, 4, 0, 0, 0, 1, 1, 1, 0,
                    0, 0, 1, 1, 1, 0, 1, 1, 1, 0,
                    0, 1, 1, 1, 1, 3, 1, 1, 0, 0,
                    0, 0, 1, 1, 1, 1, 1, 1, 1, 0,
                    0, 1, 0, 1, 0, 1, 0, 1, 0, 0,
                    5, 0, 0, 0, 0, 4, 0, 0, 0, 5,
                    ]
                    }

    def generate(self, lev_list):
        self.blocks.clear()
        self.rats.clear()
        self.sprites.clear()
        x = 0
        y = 0
        for _ in lev_list:  # Places corresponding game object as it relates to list values
            if lev_list[x + (y*10)] == 1:
                Block((x, y))

            if lev_list[x + (y*10)] == 2:
                self.sprites["raccoon"] = Raccoon([x, y])

            if lev_list[x + (y*10)] == 3:
                self.sprites["trash"] = Trash([x, y])

            if lev_list[x + (y*10)] == 4:
                RatSide([x, y])

            if lev_list[x + (y*10)] == 5:
                RatUp([x, y])

            x += 1
            if x > 9:
                x = 0
                y += 1

    def lev_up(self):  # Increases level
        global titling
        levelup_sound.play(0)
        fade(levelup_image)
        quit_check()
        sleep(1.5)
        self.level_num += 1
        try:
            self.generate(self.levels[self.level_num])
        except KeyError:
            write("Final Time: " + str(round(time() - timer, 2)) + " seconds", (25, 635), (0, 255, 0))
            pygame.display.flip()
            sleep(4.5)
            self.level_num = 1
            titling = True

    def restart(self):  # restarts game
        global titling
        death_sound.play(0)
        fade(death_image)

        # failure text
        heart_count = len(hearts)
        if heart_count == 5:
            write("try not to do that again", (70, 290), black)
            write("they should be fine", (100, 360), black)
            pygame.display.flip()
            heart_minus()
        if heart_count == 4:
            write("again? seriously?", (135, 325), black)
            pygame.display.flip()
            heart_minus()
        if heart_count == 3:
            write("stop.", (285, 290), red)
            write("you are hurting them.", (80, 360), black)
            pygame.display.flip()
            heart_minus()
        if heart_count == 2:
            write("you are on", (210, 290), red)
            write("the verge of death", (120, 360), red)
            pygame.display.flip()
            heart_minus()
        if heart_count == 1:
            music.pause()
            death_surf = pygame.Surface((700, 700), pygame.SRCALPHA)
            death_surf.fill(black)
            fade(death_surf)
            titling = True

        try:
            hearts.popitem()
        except KeyError:
            pass

        self.generate(self.levels[self.level_num])
        pygame.display.flip()


# Objects & Functions
title = Title((0, 0))
start_button = StartButton((290, 380))
quit_button = QuitButton((295, 505))
level = Level()


def heart_minus():  # minus heart text
    sleep(1)
    write("-1", (645, 0), red)
    pygame.display.flip()
    sleep(1.75)


def draw(class_name):  # draws sprites from classes on win
    win.blit(class_name.image, class_name.rect)


def write(words, pos, color):  # writes text on win
    game_text = font.render(words, True, color)
    win.blit(game_text, pos)


def quit_check():  # shortened quit checker
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()


def fade(image):  # fades out screen
    for alpha in range(300):
        quit_check()
        image.set_alpha(alpha)
        win.blit(image, (0, 0))
        pygame.display.update()


music.play(-1)
# Game Loop
while True:
    if titling:
        music.pause()
        title_music.play(-1)

    else:
        title_music.fadeout(2000)
        music.unpause()

    clock.tick(60)
    quit_check()

    # Title Screen
    while titling:
        clock.tick(60)
        win.fill(white)
        hearts[5] = Hearts((630, 0))
        hearts[4] = Hearts((565, 0))
        hearts[3] = Hearts((500, 0))
        hearts[2] = Hearts((435, 0))
        hearts[1] = Hearts((370, 0))
        level.level_num = 1
        title.update(.05)

        mouse = pygame.mouse.get_pos()
        start_button.hover(mouse)
        quit_button.hover(mouse)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_button.image = start_button.hovered
                    pygame.draw.rect(win, white, (290, 380, 300, 300))
                    draw(start_button)
                    pygame.display.flip()
                    timer = time()
                    sleep(.4)
                    level.generate(level.levels[level.level_num])
                    titling = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(mouse):
                    level.generate(level.levels[level.level_num])
                    titling = False
                    timer = time()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.rect.collidepoint(mouse):
                    pygame.quit()
                    exit()

    win.fill(white)
    keys_pressed = pygame.key.get_pressed()

    sprites["raccoon"].update(keys_pressed)
    sprites["trash"].update(keys_pressed)

    for b in blocks:
        draw(b)
    for r in rats:
        r.update()

    # tutorial level text
    if level.level_num == 1:
        write("the raccoon &", (20, 10), gray)
        write("the trash move contrary.", (20, 75), gray)
        write("if they strike the rats,", (20, 565), gray)
        write("it won't be merry.", (20, 635), gray)

    for k in hearts:
        draw(hearts[k])
        hearts[k].update(.05)

    sprites["trash"].collide()
    
    pygame.display.flip()
