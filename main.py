# DEDICATED TO EMILY

# Initial Setup
import pygame
from random import randint
from sys import exit
from time import sleep

pygame.init()
win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Racoonundrum - a trashy game")

# Variables
clock = pygame.time.Clock()
music = pygame.mixer.music
blocks, rats = [], []
sprites = {}
size = 70
white = (255, 255, 255)
isTitle = True

# Music & Sounds
music.load("assets/background_music.wav")

title_music = pygame.mixer.Sound("assets/title_theme.wav")
button_sound = pygame.mixer.Sound("assets/button_sound.wav")
death_sound = pygame.mixer.Sound("assets/death_sound.wav")
levelup_sound = pygame.mixer.Sound("assets/complete_sound.wav")

# Art
death_image = pygame.image.load("assets/death.jpg")
levelup_image = pygame.image.load("assets/complete.jpg")

# Tutorial
font = pygame.font.Font("assets/font.ttf", 50)
tutorial_text = [
    font.render("the raccoon and the trash", True, (30, 30, 30)), 
    font.render("move contrary.", True, (30, 30, 30)),
    font.render("if they strike the rats,", True, (30, 30, 30)),
    font.render("it won't be merry.", True, (30, 30, 30)),
    font.render("try not to do that again", True, (0, 0, 0)),
    font.render("they should be fine...", True, (0, 0, 0)),
    font.render("again? seriously?", True, (0, 0, 0)),
    font.render("stop. you're hurting them.", True, (255, 0, 0)),
    ]
                

# Classes
class Maze(object):
    def __init__(self):
        self.image = pygame.Surface((700, 700))
        self.rect = self.image.get_rect()

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Title(Maze):
    def __init__(self, pos):
        super().__init__()
        self.images = [
            pygame.image.load("assets/title0.jpg"),
            pygame.image.load("assets/title1.jpg"),
            ]
        self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        self.current_image += .003
        if int(self.current_image) >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.draw(win)


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

    def hover(self, mouse):
        if self.rect.collidepoint(mouse):
            if not self.over:
                button_sound.play(0)
                self.over = True
            self.image = self.hovered
            self.draw(win)

        if not self.rect.collidepoint(mouse):
            self.over = False
            self.update()


class QuitButton(StartButton):
    def __init__(self, pos):
        super().__init__(pos)
        self.hovered = pygame.image.load("assets/quit_hover.png")
        self.images = [
            pygame.image.load("assets/quit0.png"),
            pygame.image.load("assets/quit1.png"),
            ]


class MazeBlock(Maze):
    def __init__(self, pos):
        super().__init__()
        blocks.append(self)
        self.images = [
            pygame.image.load("assets/block0.jpg"),
            pygame.image.load("assets/block1.jpg"),
            pygame.image.load("assets/block2.jpg"),
            pygame.image.load("assets/block3.jpg"),
            ]
        self.image = self.images[randint(0, 3)]
        self.rect = pygame.Rect(pos[0]*size, pos[1]*size, size, size)


class Raccoon(Maze):
    def __init__(self, pos):
        super().__init__()
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
        if self.isTrash:
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

        self.draw(maze.image)


class MazeTrash(Raccoon):
    def __init__(self, pos):
        super().__init__(pos)
        self.images = [
            pygame.image.load("assets/trash0.png"),
            pygame.image.load("assets/trash1.png"),
            pygame.image.load("assets/trash2.png"),
            pygame.image.load("assets/trash3.png"),
            ]
        self.image = self.images[2]
        self.rect = pygame.Rect(pos[0]*size, pos[1]*size, 45, 45)
        self.rect.x += 12
        self.rect.y += 12
        self.isTrash = True

    def collide(self):
        if self.rect.colliderect(sprites["raccoon"].rect):
            level.lev_up()


class MazeRatUp(Maze):
    def __init__(self, pos):
        super().__init__()
        rats.append(self)
        self.images = [
            pygame.transform.rotate(pygame.image.load("assets/rats0.png"), 180),
            pygame.transform.rotate(pygame.image.load("assets/rats1.png"), 0),
            pygame.transform.rotate(pygame.image.load("assets/rats0.png"), 270),
            pygame.transform.rotate(pygame.image.load("assets/rats1.png"), 90),
            ]
        self.image = self.images[0]
        self.rect = pygame.Rect(pos[0]*size, pos[1]*size, 70, 70)
        self.hitrect = pygame.Rect(pos[0]*size, pos[1]*size, 40, 55)
        self.hitrect.center = self.rect.center
        self.vel = 4

    def collide(self):
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
        if self.vel == -4:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        self.rect.y += self.vel
        self.hitrect.y += self.vel

        self.collide()


class MazeRatSide(MazeRatUp):
    def __init__(self, pos):
        super().__init__(pos)
        rats.append(self)
        self.image = self.images[2]
        self.hitrect = pygame.Rect(pos[0]*size, pos[1]*size, 55, 40)
        self.hitrect.center = self.rect.center
        self.vel = 2

    def update(self):
        self.rect.x += self.vel
        self.hitrect.x += self.vel
        if self.vel == -2:
            self.image = self.images[2]
        else:
            self.image = self.images[3]

        self.collide()
            

class Level(object):
    def __init__(self):
        self.level_num = 1
        self.deaths = 0
        self.sprites = sprites
        self.blocks = blocks
        self.rats = rats
        self.levels = {
                2: [  # hashtag
                    1, 1, 1, 5, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 3, 0, 0, 0, 0, 0, 0, 0, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 0, 0, 0, 0, 2, 1,
                    1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 0, 1, 1, 5, 1, 1, 1,
                    ],

                3: [  # tricky
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

                5: [  # tutorial
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

                4: [  # rapunzel
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
                    ],

                1: [  # upside
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
                    }

    def generate(self, lev_list):
        self.blocks.clear()
        self.rats.clear()
        self.sprites.clear()
        x = 0
        y = 0
        for _ in lev_list:
            if lev_list[x + (y*10)] == 1:
                MazeBlock((x, y))

            if lev_list[x + (y*10)] == 2:
                self.sprites["raccoon"] = Raccoon([x, y])

            if lev_list[x + (y*10)] == 3:
                self.sprites["trash"] = MazeTrash([x, y])

            if lev_list[x + (y*10)] == 4:
                MazeRatSide([x, y])

            if lev_list[x + (y*10)] == 5:
                MazeRatUp([x, y])

            x += 1
            if x > 9:
                x = 0
                y += 1

    def lev_up(self):
        global isTitle
        levelup_sound.play(0)
        fade((255, 255, 250))
        win.fill(white)
        win.blit(levelup_image, (0, 0))
        pygame.display.flip()
        quit_check()
        sleep(3)
        self.level_num += 1
        try:
            self.generate(self.levels[self.level_num])
        except KeyError:
            self.level_num = 1
            isTitle = True

    def restart(self):
        death_sound.play(0)
        fade((150, 0, 0))
        win.blit(death_image, (0, 0))
        pygame.display.flip()

        if self.deaths == 0:
            win.blit(tutorial_text[4], (70, 290))
            win.blit(tutorial_text[5], (90, 360))
            pygame.display.flip()
            sleep(4)

        if self.deaths == 1:
            win.blit(tutorial_text[6], (130, 320))
            pygame.display.flip()
            sleep(4)

        if self.deaths == 2:
            win.blit(tutorial_text[7], (25, 320))
            pygame.display.flip()
            sleep(4)

        self.deaths += 1
        sleep(1.75)
        self.generate(self.levels[self.level_num])
        pygame.display.flip()


# Objects & Functions
title = Title((0, 0))
start_button = StartButton((290, 375))
quit_button = QuitButton((295, 505))
level = Level()
maze = Maze()


def quit_check():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()


def fade(color):
    fade_win = pygame.Surface((700, 700))
    fade_win.fill(color)
    for alpha in range(0, 280):
        quit_check()
        maze.draw(win)
        fade_win.set_alpha(alpha)
        win.blit(fade_win, (0, 0))
        pygame.display.update()


music.play(-1)
# Game Loop
while True:
    if isTitle:
        music.pause()
        title_music.play(-1)

    else:
        title_music.fadeout(2000)
        music.unpause()

    clock.tick(60)
    quit_check()

    # Title Screen
    while isTitle:
        win.fill(white)
        title.update()

        mouse = pygame.mouse.get_pos()
        start_button.hover(mouse)
        quit_button.hover(mouse)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.rect.collidepoint(mouse):
                    pygame.quit()
                    exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(mouse):
                    level.generate(level.levels[level.level_num])
                    isTitle = False

    win.fill((255, 255, 255))
    maze.draw(win)
    maze.image.fill((255, 255, 255))
    
    keys_pressed = pygame.key.get_pressed()
    sprites["raccoon"].update(keys_pressed)
    sprites["trash"].update(keys_pressed)

    # tutorial text
    if level.level_num == 0:
        win.blit(tutorial_text[0], (30, 10))
        win.blit(tutorial_text[1], (170, 75))
        win.blit(tutorial_text[2], (80, 565))
        win.blit(tutorial_text[3], (130, 635))

    for b in blocks:
        b.draw(maze.image)

    for r in rats:
        r.draw(maze.image)
        r.update()

    sprites["trash"].collide()
    
    pygame.display.flip()
