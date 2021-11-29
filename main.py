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
MUSIC = pygame.mixer.music
BLOCKS, RATS = [], []
SIZE = 70
TITLE = True
BUTTON_PRESSED = False
BUTTON_PRESSED1 = False

# Music & Sounds
MUSIC.load("assets/background_music.wav")

TITLE_MUSIC = pygame.mixer.Sound("assets/title_theme.wav")
BUTTON_SOUND = pygame.mixer.Sound("assets/button_sound.wav")
DEATH_SOUND = pygame.mixer.Sound("assets/death_sound.wav")
LEVELUP_SOUND = pygame.mixer.Sound("assets/complete_sound.wav")

# Art
BLOCK_IMAGES = [
    pygame.image.load("assets/block0.jpg"),
    pygame.image.load("assets/block1.jpg"),
    pygame.image.load("assets/block2.jpg"),
    pygame.image.load("assets/block3.jpg"),
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

TITLE_SCREEN = [
    pygame.image.load("assets/title0.jpg"),
    pygame.image.load("assets/title1.jpg"),
    ]

TITLE_BLANK = pygame.image.load("assets/title_blank.jpg")

START_BUTTON = [
    pygame.image.load("assets/start0.png"),
    pygame.image.load("assets/start1.png"),
    ]

QUIT_BUTTON = [
    pygame.image.load("assets/quit0.png"),
    pygame.image.load("assets/quit1.png"),
    ]

START_HOVERED = pygame.image.load("assets/start_hover.png")
QUIT_HOVERED = pygame.image.load("assets/quit_hover.png")

END_IMAGE = pygame.image.load("assets/the_end.jpg")
DEATH_IMAGE = pygame.image.load("assets/death.jpg")
LEVELUP_IMAGE = pygame.image.load("assets/complete.jpg")


# Classes
class Maze(object):
    def __init__(self):
        self.image = pygame.Surface((700, 700))
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Raccoon(Maze):
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


class MazeBlock(Maze):
    def __init__(self, pos):
        super().__init__()
        BLOCKS.append(self)
        self.image = BLOCK_IMAGES[randint(0, 3)]
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, SIZE, SIZE)


class Title(Maze):
    def __init__(self, pos, image_list):
        super().__init__()
        self.images = image_list
        self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, hovered):
        if hovered:
            WIN.blit(self.image, self.rect)
            return

        self.current_image += .003
        if int(self.current_image) >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]
        WIN.blit(self.image, self.rect)


class Button(Title):
    def __init__(self, pos, image_list):
        super().__init__(pos, image_list)
        self.images = image_list
        self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))


class MazeRatUp(Maze):
    def __init__(self, pos):
        super().__init__()
        RATS.append(self)
        self.image = RAT_IMAGES[0]
        self.rect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 70, 70)
        self.hitrect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 40, 55)
        self.hitrect.center = self.rect.center
        self.vel = 4

    def collide(self):
        for block in BLOCKS:
            if self.rect.colliderect(block.rect):
                self.vel *= -1

        if self.rect.left <= 0 or self.rect.right >= 701:
            self.vel *= -1

        if self.rect.top <= 0 or self.rect.bottom >= 701:
            self.vel *= -1

        if self.hitrect.colliderect(trash.rect):
            level.restart()

        if self.hitrect.colliderect(raccoon.rect):
            level.restart()

    def update(self):
        if self.vel == -4:
            self.image = RAT_IMAGES[0]
        else:
            self.image = RAT_IMAGES[1]
        self.rect.y += self.vel
        self.hitrect.y += self.vel

        self.collide()


class MazeRatSide(MazeRatUp):
    def __init__(self, pos):
        super().__init__(pos)
        RATS.append(self)
        self.image = RAT_IMAGES[2]
        self.hitrect = pygame.Rect(pos[0]*SIZE, pos[1]*SIZE, 55, 40)
        self.hitrect.center = self.rect.center
        self.vel = 2

    def update(self):
        self.rect.x += self.vel
        self.hitrect.x += self.vel
        if self.vel == -2:
            self.image = RAT_IMAGES[2]
        else:
            self.image = RAT_IMAGES[3]

        self.collide()
            

class Level(object):
    def __init__(self):
        self.level_num = 1
        self.blocks = BLOCKS
        self.rats = RATS
        self.levels = {
                3: [  # hashtag
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

                4: [  # tricky
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

                2: [  # beginner
                    1, 1, 1, 1, 0, 0, 0, 0, 0, 3,
                    1, 0, 1, 1, 0, 0, 1, 1, 1, 1,
                    1, 1, 1, 1, 5, 5, 0, 1, 0, 1,
                    1, 1, 1, 1, 0, 0, 1, 1, 1, 0,
                    1, 1, 1, 0, 0, 0, 1, 1, 1, 1,
                    1, 1, 1, 1, 0, 0, 0, 1, 1, 1,
                    0, 1, 1, 1, 0, 0, 1, 1, 0, 1,
                    1, 1, 1, 0, 0, 0, 1, 1, 1, 1,
                    1, 1, 1, 1, 0, 0, 1, 1, 0, 1,
                    2, 0, 0, 0, 0, 0, 1, 1, 1, 1,
                    ],

                1: [  # charlie's level
                    1, 1, 1, 1, 1, 1, 0, 3, 1, 1,
                    1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
                    1, 1, 1, 1, 5, 1, 0, 1, 1, 1,
                    1, 1, 1, 1, 0, 1, 0, 1, 1, 1,
                    4, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                    0, 0, 0, 0, 4, 0, 4, 0, 0, 0,
                    1, 1, 1, 1, 0, 1, 0, 1, 1, 1,
                    1, 1, 1, 1, 0, 1, 5, 1, 1, 1,
                    1, 1, 1, 1, 0, 1, 1, 1, 1, 1,
                    1, 1, 1, 2, 0, 1, 1, 1, 1, 1,
                    ],
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
                MazeRatSide([x, y])

            if lev_list[x + (y*10)] == 5:
                MazeRatUp([x, y])

            x += 1
            if x > 9:
                x = 0
                y += 1
    
    def lev_up(self):
        global TITLE
        LEVELUP_SOUND.play(0)
        fade((255, 255, 250))
        WIN.fill((0, 208, 0))
        WIN.blit(LEVELUP_IMAGE, (10, 10))
        pygame.display.flip()
        quit_check()
        sleep(3)
        self.level_num += 1
        try:
            self.generate(self.levels[self.level_num])
        except KeyError:
            self.level_num = 1
            TITLE = True

    def restart(self):
        DEATH_SOUND.play(0)
        fade((150, 0, 0))
        WIN.blit(DEATH_IMAGE, (10, 10))
        pygame.display.flip()
        sleep(1.5)
        self.generate(self.levels[self.level_num])


# Objects & Functions
title_screen = Title((10, 10), TITLE_SCREEN)
start_button = Button((300, 385), START_BUTTON)
quit_button = Button((305, 515), QUIT_BUTTON)
level = Level()
maze = Maze()


def quit_check():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()


def fade(color):
    fade_win = pygame.Surface((720, 720))
    fade_win.fill(color)
    for alpha in range(0, 280):
        quit_check()
        maze.draw(WIN)
        fade_win.set_alpha(alpha)
        WIN.blit(fade_win, (0, 0))
        pygame.display.update()


MUSIC.play(-1)
# Game Loop
while True:
    if TITLE:
        MUSIC.pause()
        TITLE_MUSIC.play(-1)

    else:
        TITLE_MUSIC.fadeout(2000)
        MUSIC.unpause()

    CLOCK.tick(60)
    quit_check()

    # Title Screen
    while TITLE:
        WIN.fill((95, 158, 160))
        WIN.blit(TITLE_BLANK, (10, 10))
        title_screen.update(False)

        mouse = pygame.mouse.get_pos()
        if start_button.rect.collidepoint(mouse):
            if not BUTTON_PRESSED:
                BUTTON_SOUND.play(0)
                BUTTON_PRESSED = True
            start_button.image = START_HOVERED
            start_button.update(True)

        if not start_button.rect.collidepoint(mouse):
            BUTTON_PRESSED = False
            start_button.update(False)

        if quit_button.rect.collidepoint(mouse):
            if not BUTTON_PRESSED1:
                BUTTON_SOUND.play(0)
                BUTTON_PRESSED1 = True
            quit_button.image = QUIT_HOVERED
            quit_button.update(True)

        if not quit_button.rect.collidepoint(mouse):
            BUTTON_PRESSED1 = False
            quit_button.update(False)

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

    WIN.fill((218, 165, 32))
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
